import logging
import os

"""
Contains the declaration of the library's logger
"""
logger = logging
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
path = os.path.join(config_path , "inejsonstat.log")
logger.basicConfig(filename=path, encoding='utf-8', level=logging.DEBUG,
                   format='%(asctime)s; %(levelname)s; %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
