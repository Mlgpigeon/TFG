from data_model.jsonutil import JsonUtil as util
from data_model.inejsonstat import IneJsonStat
from data_model.main_logger import logger
from data_model.url_builder import UrlBuilder as url_build
from data_model.jsonstatrequest import JsonStatRequest
from data_model.languages_enum import LanguageEnum
from data_model.target_enum import TargetEnum


class IneInitializer:

    @staticmethod
    def create2(target: str = None, language: str = None, date: str = None, datetype: str = None, nult = None):
        if target is not None:
            if type(target) is TargetEnum:
                print("Target is enum")
                target = target.value
        target_in = target

        if language is not None:
            if type(language) is LanguageEnum:
                print("Language is enum")
                language = language.value
        language_in = language

        if date is not None:
            date = util.date_conversor(date, datetype)
        date_in = date

        if nult is not None:
            if type(nult) is int:
                nult_url = nult
            elif type(nult) is str:
                if util.check_int(nult):
                    nult_url = nult
                else:
                    raise Exception("nult is not an integer")
        else:
            nult_in = None

        request = JsonStatRequest(target_in, language_in, date_in, nult_in)

        return request

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

