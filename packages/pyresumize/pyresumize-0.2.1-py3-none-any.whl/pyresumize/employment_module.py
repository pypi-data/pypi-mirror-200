import os
import spacy
from pyresumize.interfaces import EmployerBaseInterface
from pyresumize.utilities import Utilities
import logging


class EmployerCustomNEREngine(EmployerBaseInterface):
    def __init__(self, config_folder) -> None:
        super().__init__(config_folder)
        self.nlp = spacy.load("en_core_web_sm", exclude=["entity_ruler"])
        self.__generate_employers()

    def __generate_employers(self):
        employ_input_folder = os.path.join(self.config_folder, "employers")
        utils = Utilities()
        employers = utils.generate_keywords_from_csv_files(employ_input_folder)
        employers = list(map(lambda x: str(x).lower(), employers))  # Normalising the Strings to Lower
        print("Generating Company Database: Found %d " % len(employers))
        patterns = []
        ruler = self.nlp.add_pipe("entity_ruler")
        for employer in employers:
            entry = {}
            entry["label"] = "EMPLOYER"
            entry["pattern"] = str(employer)
            patterns.append(entry)
        ruler.add_patterns(patterns)
        self.nlp.to_disk("employers")
        self.nlp_entity = spacy.load("employers")
        self.nlp.remove_pipe("entity_ruler")
        self.nlp.add_pipe("entity_ruler", source=self.nlp_entity)

    def process(self, employment_text):
        """Process the Custom Entity EMPLOYER"""

        doc = self.nlp(employment_text.lower())
        candidate_employment = []
        for ent in doc.ents:
            if ent.label_ == "EMPLOYER":
                candidate_employment.append(ent.text.lower())
                # print(ent.text)
                # print(ent.label_)
        # Removes Duplicate
        candidate_employment = set(candidate_employment)
        return candidate_employment


class EmployerStandardEngine(EmployerBaseInterface):
    def __init__(self, nlp, config_folder) -> None:
        super().__init__(config_folder)
        self.nlp = nlp

    def process(self, employment_text):
        """does nothing"""
        candidate_employment = []
        nlp_text = self.nlp(employment_text)
        tokens = [token.text for token in nlp_text if not token.is_stop]
        employ_input_folder = os.path.join(self.config_folder, "employers")
        utils = Utilities()
        employers = utils.generate_keywords_from_csv_files(employ_input_folder)
        employers = list(map(lambda x: str(x).capitalize(), employers))  # Normalising the Strings to Lower
        logging.info("found %d employers " % len(employers))

        candidate_employment = []

        # Lets look at the companies with single word
        for token in tokens:
            token = token.capitalize()
            if token in employers:
                # if token not in candidate_employment:
                candidate_employment.append(token)

        # for the Combined names  such as Operating Systems
        for token in nlp_text.noun_chunks:
            token = token.text.capitalize().strip()
            if token in employers:
                candidate_employment.append(token)

        candidate_employment = set(candidate_employment)
        return candidate_employment
