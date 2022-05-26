from data_model.jsonutil import JsonUtil as util
from data_model.inejsonstat import IneJsonStat
from data_model.main_logger import logger
from data_model.url_builder import UrlBuilder as url_build


class IneInitializer:
    @staticmethod
    # Initializes the object's attributes with an input log filename and an input yaml file
    def create(input_yaml):
        logger.debug("IneInitializer || Initializing IneInitializer")
        ine_instance = IneJsonStat()

        yaml_data = util.read_config_yaml(input_yaml)

        ine_instance.set_yaml_data(yaml_data)

        flag_build, url = url_build.build_url(yaml_data)

        if flag_build:
            logger.info('IneInitializer || URL working, starting dataset generation')
            ine_instance.set_url(url)
            dataset = ine_instance.generate_object()
            return dataset
        else:
            return False

