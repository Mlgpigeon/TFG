import logging
import os

logger = logging
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config_files"))
#print(config_path)
logger.basicConfig(filename=config_path +"\inejsonstat.log", encoding='utf-8', level=logging.DEBUG,
                   format='%(asctime)s; %(levelname)s; %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
