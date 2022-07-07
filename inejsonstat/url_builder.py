import json
import os
from urllib.request import urlopen

import jsonstatpy
from inejsonstat.jsonutil import JsonUtil as util
from inejsonstat.main_logger import logger


class UrlBuilder:
    """
    Class tasked with building a valid request URL for the INE's JSON-stat API and generating a cache copy
    """
    @staticmethod
    def check_input(input_url, input_str):
        """Checks if the input_url is reachable and input_str denotes if its parameterized or not.

            Parameters
            ----------
            input_url: string
            input_str: string

            Returns
            -------
            A boolean flag if the file has been recovered correctly and a JsonStatDataSet
            from the jsonstat.py library reflecting the recovered data.
            """
        flag_url = False
        json_data = None
        try:
            response = urlopen(input_url)
            json_data = json.loads(response.read())
            if json_data is not None:
                logger.info("UrlBuilder || URL " + input_str + " working")
                flag_url = True

        except Exception as e:
            exception_message = 'UrlBuilder || Module [check_input], URL ' + input_str + " not working" + str(e)
            logger.debug(exception_message)
            print("URL " + input_str + " not working")

        return flag_url, json_data

    @staticmethod
    # Builds the URL for retrieving the JSON based on the config file parameters
    def build_url(target, language, date: str = None, nult: int = None):
        """Builds a valid INE JSON-stat API URL and makes the request.

                Parameters
                ----------
                target : string
                language : string
                date : string
                nult  : string
                Returns
                -------
                A boolean flag if the file has been recovered correctly, a JsonStatDataSet
                from the jsonstat.py library reflecting the recovered data and the URL executed.
        """
        logger.info("UrlBuilder2 || Executing module [build_url]")
        base_url = "https://servicios.ine.es/wstempus/jsstat/"
        data_type = "DATASET"
        flag_extraparams = False

        # URL base building
        unparameterized_url = base_url + language + "/" + data_type + "/" + target
        logger.info("Unparameterized url is;" + str(unparameterized_url))
        url = unparameterized_url
        flag_working = True

        if nult is not None:
            flag_extraparams = True
            if type(nult) is int:
                nult = str(nult)
            url = url + "?nult=" + nult

        if date is not None:
            flag_extraparams = True
            url = url + "?date=" + date

        if flag_extraparams:
            flag_working, json_data = UrlBuilder.check_input(url, "parameterized")
            info_message = "The URL is: " + url
            logger.info(info_message)

            if not flag_working:
                logger.debug("UrlBuilder || Retrying url with forcefully unparameterized url")
                flag_working, json_data = UrlBuilder.check_input(unparameterized_url, "forcefully unparameterized")
                info_message = "The URL is: " + url
                logger.info(info_message)
                if flag_working:
                    logger.debug("UrlBuilder || Error in parameter, forcing unparameterized url")
                if not flag_working:
                    logger.debug("UrlBuilder || Error in url basic definition")

        if not flag_extraparams:
            flag_working = UrlBuilder.check_input(unparameterized_url, "unparameterized")
            info_message = "UrlBuilder || The URL is: " + unparameterized_url
            logger.info(info_message)
            url = unparameterized_url
            if flag_working:
                logger.info("UrlBuilder || Basic URL definition successful")
            if not flag_working:
                logger.debug("UrlBuilder || Error in url basic definition")

        if flag_working:
            file_name = util.file_name_builder(target, language, date, nult)
            UrlBuilder.create_cache_file(json_data, file_name)
            # get path of cache folder in parent directory
            cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cache"))
            path = os.path.join(cache_path, file_name + ".json")
            json_stat_data = jsonstatpy.from_file(path)
        return flag_working, json_stat_data, url

    @staticmethod
    def create_cache_file(json_data, file_name):
        """Creates a json file in cache from the json_data with the file_name as the file name.

                Parameters
                ----------
                json_data : JsonStatDataSet from the jsonstat.py library
                file_name : string

        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cache"))
        if not os.path.exists(path):
            os.makedirs(path)
        search_path = os.path.join(path, file_name + '.json')
        with open(search_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
