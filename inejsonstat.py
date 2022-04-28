import logging
import re

import jsonstat
import yaml


# Class that defines the category of a dimension
class JsonStatCategory:
    def __init__(self, index, label, size):
        self.index = index
        self.label = label
        self.size = size


# Class that defines a dimension of a json-stat dataset
class JsonStatDimension:
    def __init__(self, name, label, category, role):
        self.name = name
        self.label = label
        self.category = JsonStatCategory(category.index, category.label, category.size)
        self.role = role


# Class that defines a json-stat dataset
class ProcJsonStatDataset:
    def __init__(self):
        self.name = 'dataset'

    # Returns a list of dimensions in the dataset
    @property
    def dimensions(self):
        return self.__dict__.items()

    # Print all dimensions of the dataset
    def printed_dimensions(self):
        print("Dimensions of dataset: ")
        for key, value in self.dimensions:
            print(key)


# Checks if the input is an integer
def check_int(input_int):
    return input_int.isdigit()


# Normalizes the string to a valid attribute name
def normalize_string(input_str):
    logging.info("Executing module [normalize_string]")
    print(input_str)

    # Convert to lower case
    lower_str = input_str.lower()
    print(lower_str)

    # remove all punctuation except words and space
    no_punc_str = re.sub(r'[^\w\s]', '', lower_str)
    print(no_punc_str)

    # Removing possible leading and trailing whitespaces
    no_trail_str = no_punc_str.strip()

    # Replace white spaces with underscores
    no_spaces_string = no_trail_str.replace(" ", "_")

    return no_spaces_string


# Checks if there's a nult parameter in the config file and if it matches the allowed format
def check_nult(nult):
    logging.info("Executing module [check_nult]")
    flag_nult = False
    if nult == '':
        logging.debug("No nult parameter")
        print("no nult")
    else:
        if check_int(nult):
            logging.info("Nult parameter valid, format: integer")
            print("nult valid")
            flag_nult = True
        else:
            logging.debug("Nult format invalid")
            print("nult invalid")
    return flag_nult


# Checks if there's a date parameter in the config file and if it matches the allowed formats
def check_date(date):
    logging.info("Executing module [check_date]")
    flag_date = False
    if date == '':
        logging.debug("Module [check_date], No date parameter")
        print("no date")
    else:
        base_pattern = r"[0-9]{4}[0-1]{1}[0-9]{1}[0-3]{1}[0-9]{1}"
        pattern1 = r"\b" + base_pattern + r"\Z"
        matcher1 = re.compile(pattern1)
        pattern2 = r"\b" + base_pattern + r"[:]" + base_pattern + r"\Z"
        matcher2 = re.compile(pattern2)
        pattern3 = r"\b" + base_pattern + r"(&" + base_pattern + r")+" + r"\Z"
        matcher3 = re.compile(pattern3)

        if matcher3.match(date):
            logging.info("Date parameter valid, format: YYYYMMDD&YYYYMMDD")
            print("Format YYYYMMDD&YYYYMMDD")
            flag_date = True
        elif matcher2.match(date):
            logging.info("Date parameter valid, format: YYYYMMDD:YYYYMMDD")
            print("Format YYYYMMDD:YYYYMMDD")
            flag_date = True
        elif matcher1.match(date):
            logging.info("Date parameter valid, format: YYYYMMDD")
            print("Format YYYYMMDD")
            flag_date = True
        else:
            exception_message = 'Module [check_date], Date parameter format invalid'
            logging.debug(exception_message)
            print("Format invalid")
    return flag_date


class IneJsonStat:
    def __init__(self):
        self.json_data = None
        self.yaml_data = None
        self.dataset = ProcJsonStatDataset()
        self.log = None
        self.url = None

    def read_json_file(self, input_url):
        try:
            self.set_json_data(jsonstat.from_url(input_url))
        except Exception as e:
            logging.debug("Error reading json file: %s", e)
            return False
        return True

    # Reads the config yaml file
    def read_config_yaml(self):
        with open("config.yaml", "r") as yaml_file:
            self.yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            logging.debug("Config file read successful")
            print("Config file read successful")

    def configure_logging(self, log_file_name):
        logging.basicConfig(filename=log_file_name, encoding='utf-8', level=logging.DEBUG,
                            format='%(asctime)s; %(levelname)s; %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        self.set_log(log_file_name)
        logging.info('--------------------------------------------------------------------------------')
        logging.info('logging configured')
        logging.info('Starting program')

    # Parameters from config
    def read_yaml_parameters(self):

        language = self.yaml_data[0]['Details']['language']
        input_table = self.yaml_data[0]['Details']['input']
        nult = self.yaml_data[0]['Details']['nult']
        date = self.yaml_data[0]['Details']['date']

        return language, input_table, nult, date

    def get_json_data(self):
        return self.json_data

    def set_json_data(self, json_data):
        self.json_data = json_data

    def get_yaml_data(self):
        return self.yaml_data

    def set_yaml_data(self, yaml_data):
        self.yaml_data = yaml_data

    def get_dataset(self):
        return self.dataset

    def set_dataset(self, dataset):
        self.dataset = dataset

    def get_log(self):
        return self.log

    def set_log(self, log):
        self.log = log

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def create(self):
        self.configure_logging('inejsonstat.log')

        flag_build = self.build_url()

        if flag_build:
            logging.info('URL working, starting dataset generation')
            self.generate_object(self.url)

    # Builds the URL for retrieving the JSON based on the config file parameters
    def build_url(self):
        logging.info("Executing module [build_url]")
        base_url = "https://servicios.ine.es/wstempus/jsstat/"
        data_type = "DATASET"
        flag_extraparams = False

        self.read_config_yaml()

        language, input_table, nult, date = self.read_yaml_parameters()

        # URL base building
        unparameterized_url = base_url + language + "/" + data_type + "/" + input_table
        url = unparameterized_url
        flag_working = True

        if check_nult(nult):
            flag_extraparams = True
            url = url + "?nult=" + nult

        if check_date(date):
            flag_extraparams = True
            url = url + "?date=" + date

        if flag_extraparams:
            flag_working = self.check_input(url, "parameterized")
            info_message = "The URL is: " + url
            logging.info(info_message)
            print(url)

            if not flag_working:
                logging.debug("Retrying url with forcefully unparameterized url")
                flag_working = self.check_input(unparameterized_url, "forcefully unparameterized")
                info_message = "The URL is: " + url
                logging.info(info_message)
                if flag_working:
                    logging.debug("Error in parameter, forcing unparameterized url")
                if not flag_working:
                    logging.debug("Error in url basic definition")

        if not flag_extraparams:
            flag_working = self.check_input(unparameterized_url, "unparameterized")
            info_message = "The URL is: " + unparameterized_url
            logging.info(info_message)
            url = unparameterized_url
            if flag_working:
                logging.info("Basic URL definition successful")
            if not flag_working:
                logging.debug("Error in url basic definition")

        if flag_working:
            self.set_url(url)

        return flag_working

    # Generate a dataset with dimensions and values
    def generate_object(self, input_url):
        logging.info("Executing module [generate_object]")

        self.read_json_file(input_url)

        size = self.get_number_dimensions()
        print(size)

        dataset = ProcJsonStatDataset()
        dimensions = self.generate_dimensions(size)

        for i in range(0, size):
            name = normalize_string(dimensions[i].name)
            setattr(dataset, name, dimensions[i])
            print(getattr(dataset, name, 'Attribute doesnt exist' + name))

        value_size, value = self.generate_value()
        setattr(dataset, 'value', value)
        setattr(dataset, 'value_size', value_size)

        status_size, status = self.generate_status()
        setattr(dataset, 'status', status)
        setattr(dataset, 'status_size', status_size)

        dataset.printed_dimensions()
        # print_data(dataset)
        self.set_dataset(dataset)

    @staticmethod
    # Checks if the input URL works correctly
    def check_input(input_url, input_str):
        logging.info("Executing module [check_input]")
        flag_url = False
        try:
            if jsonstat.from_url(input_url) is not None:
                print("URL " + input_str + " working")
                logging.info("URL " + input_str + " working")
                flag_url = True
        except Exception as e:
            exception_message = 'Module [check_input], URL ' + input_str + " not working" + str(e)
            logging.debug(exception_message)
            print("URL " + input_str + " not working")
        return flag_url

    # Getting the number of dimensions
    def get_number_dimensions(self):
        logging.info("Executing module [get_number_dimensions]")
        exit_flag = False
        i = 0
        while not exit_flag:
            try:
                self.json_data.dimension(i)
                i = i + 1
            except Exception as e:
                exception_message = 'Module [get_number_dimensions], limit position: ' + str(i) + ", " + str(e)
                logging.debug(exception_message)
                exit_flag = True
        return i

    @staticmethod
    # Getting the size of the category of a given dimension
    def calculate_category_size(dimension):
        logging.info("Executing module [calculate_category_size]")
        exit_flag = False
        i = 0
        while not exit_flag:
            try:
                if dimension.category(i).index is not None:
                    i = i + 1
            except Exception as e:
                exception_message = 'Module [calculate_category_size], limit position: ' + str(i) + ", " + str(e)
                logging.debug(exception_message)
                exit_flag = True
        return i

    @staticmethod
    # Checks if the dimension has an index
    def check_index(dimension):
        logging.info("Executing module [check_index]")
        flag_index = False
        try:
            index = dimension.category(0).index
            flag_index = True
            if index == '':
                flag_index = False
                print("no index")
        except Exception as e:
            exception_message = 'Module [check_index], no index, ' + str(e)
            logging.debug(exception_message)
            print("no index")
        return flag_index

    @staticmethod
    # Checks if the dimension has a label
    def check_label(dimension):
        logging.info("Executing module [check_label]")
        flag_label = False
        try:
            label = dimension.category(0).label
            flag_label = True
            if label == '':
                flag_label = False
                print("no label")
        except Exception as e:
            exception_message = 'Module [check_label], no label, ' + str(e)
            logging.debug(exception_message)
            print("no label")
        return flag_label

    # Generates an index and a label for a dimension category if they exist
    def generate_index(self, dimension, size):
        logging.info("Executing module [generate_index]")
        index = dict()
        label = dict()

        has_index = self.check_index(dimension)
        has_label = self.check_label(dimension)

        if has_index:
            for i in range(0, size):
                index[i] = dimension.category(i).index

        if has_label:
            for i in range(0, size):
                label[index[i]] = dimension.category(i).label
        return index, label

    # Generates the category for a dimension
    def generate_category(self, dimension):
        logging.info("Executing module [generate_category]")
        size = self.calculate_category_size(dimension)
        logging.info("Size of category: " + str(size))
        print("Size of category: ", size)
        index, label = self.generate_index(dimension, size)
        logging.info("Index: " + str(index))
        logging.info("Label: " + str(label))
        print("index: ", index)
        print("label: ", label)
        print("size: ", size)
        category = JsonStatCategory(index, label, size)
        return category

    # Generates the dimensions for a dataset
    def generate_dimensions(self, size):
        logging.info("Executing module [generate_dimensions]")
        dimensions = []
        # print(collection.dimension(0).category(0).index)
        for i in range(0, size):
            category = self.generate_category(self.json_data.dimension(i))
            role = self.json_data.dimension(i).role
            dimension = JsonStatDimension(self.json_data.dimension(i).did, self.json_data.dimension(i).label,
                                          category, role)
            dimensions.append(dimension)
        return dimensions

    # Getting the size of the category of a given dimension
    def generate_status(self):
        logging.info("Executing module [generate_status]")
        exit_flag = False
        status = []
        i = 0
        while not exit_flag:
            try:
                status.append(self.json_data.status(i))
                i = i + 1
            except Exception as e:
                exception_message = 'Module [generate_status], limit position: ' + str(i) + ", " + str(e)
                logging.debug(exception_message)
                exit_flag = True
        return i, status

    # Getting the values of the collection
    def generate_value(self):
        logging.info("Executing module [generate_value]")
        exit_flag = False
        value = []
        i = 0
        while not exit_flag:
            try:
                value.append(self.json_data.value(i))
                i = i + 1
            except Exception as e:
                exception_message = 'Module [generate_value], limit position: ' + str(i) + ", " + str(e)
                logging.debug(exception_message)
                exit_flag = True

        return i, value
