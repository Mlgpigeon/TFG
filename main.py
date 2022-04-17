import jsonstat
import yaml
import re
import os
import pandas as pd


# Builds the request url based on the data in the config.yaml
def check_int(int):
    return int.isdigit()

# Checks if there's a nult parameter in the config file and if it matches the allowed format
def check_nult(nult):
    flag_nult = False
    if nult == '':
        print("no nult")
    else:
        if check_int(nult):
            print("nult valid")
            flag_nult = True
        else:
            print("nult invalid")
    return flag_nult


# Checks if there's a date parameter in the config file and if it matches the allowed formats
def check_date(date):
    flag_date = False
    if date == '':
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
            print("Formato YYYYMMDD&YYYYMMDD")
            flag_date = True
        elif matcher2.match(date):
            print("Formato YYYYMMDD:YYYYMMDD")
            flag_date = True
        elif matcher1.match(date):
            print("Formato YYYYMMDD")
            flag_date = True

    return flag_date


# Checks if the input URL works correctly
def check_input(url, str):
    flag_url= False
    try:
        collection = jsonstat.from_url(url)
        print("URL " + str + " working")
        flag_url = True
    except:
        print("invalid url")
    return flag_url


# Builds the URL for retrieving the JSON based on the config file parameters
def build_url():
    base_url = "https://servicios.ine.es/wstempus/jsstat/"
    type = "DATASET"
    flag_working = False
    flag_extraparams = False

    # Reading config file
    with open("config.yaml", "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("Config file read successful")
    print(config)

    # Parameters from config
    language = config[0]['Details']['language']
    input = config[0]['Details']['input']
    nult = config[0]['Details']['nult']
    date = config[0]['Details']['date']

    # URL base building
    url = base_url+language+"/"+type+"/"+input

    # Checking if the base URL with only input works
    flag_working = check_input(url, "basic")
    print(url)

    if flag_working:

        if check_nult(nult):
            flag_extraparams = True
            url = url + "?nult=" + nult

        if check_date(date):
            flag_extraparams = True
            url = url + "?date=" + date

        if flag_extraparams:
            flag_working = check_input(url, "parameterized")
            print(url)
    return flag_working, url


# Getting the number of dimensions
def get_ndimension(collection):
    exit = False
    i = 0
    while not exit:
        try:
            collection.dimension(i)
            i= i+1
        except:
            exit = True
    return i


# Class that defines the category of a dimension
class JsonStatCategory:
    def __init__(self,index,label):
        self.index = index
        self.label = label


# Class that defines a dimension of a json-stat dataset
class JsonStatDimension:
    def __init__(self, name, label,category):
        self.name = name
        self.label = label
        self.category = JsonStatCategory(category.index,category.label)


class ProcJsonStatDataset:

    def __init__(self):
        name = 'dataset'

    # Returns a list of dimensions in the dataset
    @property
    def dimensions(self):
        return self.__dict__.keys()

    # Print all dimensions of the dataset
    @property
    def print_dimensions(self):
        for dimension in self.dimensions:
            print(dimension)


# Getting the size of the category of a given dimension
def calculate_cat_size(dimension):
    exit = False
    i = 0
    while not exit:
        try:
            dimension.category(i).index
            i = i+1
        except:
            exit = True
    return i


def check_index(dimension):
    flag_index = False
    try:
        index = dimension.category(0).index
        flag_index = True
        if (index == ''):
            flag_index = False
            print("no index")
    except:
        print("no index")
    return flag_index


def check_label(dimension):
    flag_label = False
    try:
        label=dimension.category(0).label
        flag_label = True
        if(label == ''):
            flag_label = False
            print("no label")
    except:
        print("no label")
    return flag_label


def generate_index(dimension, size):
    index = dict()
    label = dict()
    has_index = False
    has_label = False

    has_index = check_index(dimension)
    has_label = check_label(dimension)

    if has_index:
        i = 0
        for i in range(0, size):
            index[i] = dimension.category(i).index
    if has_label:
        i = 0
        for i in range(0, size):
            label[index[i]] = dimension.category(i).label
    return index,label


def generate_category(dimension):
    size = calculate_cat_size(dimension)
    print("Size of category: ", size)
    index,label = generate_index(dimension, size)
    print("index: ", index)
    print("label: ", label)
    category = JsonStatCategory(index, label)
    return category


def generate_dimensions(collection,size):
    i=0
    dimensions = []
    #print(collection.dimension(0).category(0).index)
    for i in range(0,size):
        category = generate_category(collection.dimension(i))
        dimension = JsonStatDimension(collection.dimension(i).did, collection.dimension(i).label,category)
        dimensions.append(dimension)
    return dimensions


# Generate an Object for every dimension
def generate_object(url):
    collection = jsonstat.from_url(url)
    size = get_ndimension(collection)
    print(size)
    dataset = ProcJsonStatDataset()
    dimensions = generate_dimensions(collection,size)
    i=0
    for i in range(0,size):
        name = dimensions[i].name
        setattr(dataset, name, dimensions[i])
        print(getattr(dataset, name, 'No existe el atributo' + name))


    #print(dataset.comunidadesautonomasyprovincias.category.label)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    flag_build, url = build_url()
    if flag_build :
        generate_object(url)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
