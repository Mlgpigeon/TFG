import logging

logger = logging
logger.basicConfig(filename="inejsonstat.log", encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s; %(levelname)s; %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')