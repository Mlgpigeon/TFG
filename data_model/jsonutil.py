import logging
import yaml
import jsonstat
import re
import unidecode
from data_model.main_logger import logger


class JsonUtil:

    # REVISADO
    @staticmethod
    # Reads the config yaml file
    def read_config_yaml(input_yaml):
        with open(input_yaml, "r") as yaml_file:
            logger.debug("JsonUtil || Opening yaml file")
            logger.debug("JsonUtil || Reading yaml file")
            yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            logger.debug("JsonUtil || Config file read successful")
            print("Config file read successful")
        return yaml_data

    @staticmethod
    # Parameters from config
    def read_yaml_parameters(yaml_data):

        language = yaml_data[0]['Details']['language']
        input_table = yaml_data[0]['Details']['input']
        nult = yaml_data[0]['Details']['nult']
        date = yaml_data[0]['Details']['date']

        return language, input_table, nult, date

    @staticmethod
    # Reads the json_file from an input url
    def read_json_file(input_url):
        try:
            json_data = (jsonstat.from_url(input_url))
        except Exception as e:
            logging.debug("Error reading json file: %s", e)
            return False
        return True, json_data

    @staticmethod
    # Checks if the input is an integer
    def check_int(input_int):
        return input_int.isdigit()

    @staticmethod
    # Normalizes the string to a valid attribute name
    def normalize_string(input_str):
        logging.info("Executing module [normalize_string]")
        if input_str[0].isdigit():
            input_str = "n" + input_str

        unaccented_string = unidecode.unidecode(input_str)
        # Convert to lower case
        lower_str = unaccented_string.lower()

        # remove all punctuation except words and space
        no_punc_str = re.sub(r'[^\w\s]', '', lower_str)

        # Removing possible leading and trailing whitespaces
        no_trail_str = no_punc_str.strip()

        # Replace white spaces with underscores
        no_spaces_string = no_trail_str.replace(" ", "_")

        return no_spaces_string

    @staticmethod
    # Normalizes the string to a valid attribute name
    def normalize_enum(input_str):
        logging.info("Executing module [normalize_enum]")
        if input_str[0].isdigit():
            input_str = "n" + input_str

        unaccented_string = unidecode.unidecode(input_str)
        # Convert to lower case
        upper_str = unaccented_string.upper()

        # remove all punctuation except words and space
        no_punc_str = re.sub(r'[^\w\s]', '', upper_str)

        # Removing possible leading and trailing whitespaces
        no_trail_str = no_punc_str.strip()

        # Replace white spaces with underscores
        no_spaces_string = no_trail_str.replace(" ", "_")

        return no_spaces_string

    @staticmethod
    def check_repeated(input_string, input_list):
        out_string = input_string
        aux_string = input_string
        i = 1
        flag = True
        while flag:
            if aux_string in input_list:
                aux_string ="N"+ str(i) + out_string
            else:
                flag = False
                out_string = aux_string

        return out_string
