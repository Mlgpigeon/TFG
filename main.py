import jsonstat
import yaml
import re


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
            check_input(url, "parameterized")
            print(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    build_url()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
