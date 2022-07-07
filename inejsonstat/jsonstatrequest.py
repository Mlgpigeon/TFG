import datetime
import os
import pathlib

import jsonstatpy
from inejsonstat.inejsonstat import IneJsonStat
from inejsonstat.jsonutil import JsonUtil as util
from inejsonstat.languages_enum import LanguageEnum
from inejsonstat.main_logger import logger
from inejsonstat.target_enum import TargetEnum
from inejsonstat.url_builder import UrlBuilder as url_build


class JsonStatRequest:
    """
    Class that manages the execution of requests and generation of a ProcJsonStatDataset through the generation of a
    IneJsonStat instance
    """
    def __init__(self, target: str = None, language: str = None, date: str = None, nult: int = None):
        self.target = target
        self.language = language
        self.date = date
        self.nult = nult
        self.languages = LanguageEnum
        self.targets = TargetEnum
        self.Ine = None
        self.last_url = None

    def do_request(self, target: str = None, language: str = None, date: str = None, datetype: str = None, nult=None):
        """Checks the parameters through JsonUtil and prepares them to build an URL or check its existence in cache.

            Parameters
            ----------
            self : JsonStatRequest
            target : string or TargetEnum
            language : string or LanguageEnum
            datetype : string
            date : string or date from datetime
            nult  : string or int

            Returns
            -------
            A JsonStatDataSet from the jsonstat.py library reflecting the recovered data.
        """
        date_url = ""
        nult_url = ""
        if target is not None:
            if type(target) is TargetEnum:
                logger.debug("Target is enum")
                target = target.value
            target_url = target
        else:
            if self.target is not None:
                target_url = self.target
            else:
                raise Exception("Target is not defined")

        if language is not None:
            if type(language) is LanguageEnum:
                logger.debug("Language is enum")
                language = language.value
            language_url = language
        else:
            if self.language is not None:
                language_url = self.language
            else:
                raise Exception("Language is not defined")

        if date is not None:
            date_url = util.date_conversor(date, datetype)
        else:
            if self.date is not None:
                date_url = self.date
        if nult is not None:
            if type(nult) is int:
                nult_url = nult
            elif type(nult) is str:
                if util.check_int(nult):
                    nult_url = nult
                else:
                    raise Exception("nult is not an integer")
        else:
            if self.nult is not None:
                nult_url = self.nult
            else:
                nult_url = nult

        flag_working, json_data = self.make_request(target_url, language_url, date_url, nult_url)

        if flag_working:
            return json_data
        else:
            raise Exception("Couldn't retrieve json data")

    def make_request(self, target: str = None, language: str = None, date: str = None, nult=None):
        """Executes the request of the file either by recovering it from cache if it exists or through UrlBuilder if
            contact with the API its needed.

                Parameters
                ----------
                self : JsonStatRequest
                target : string
                language : string
                date : string
                nult  : string

                Returns
                -------
                A boolean flag if the file has been recovered correctly and a JsonStatDataSet
                from the jsonstat.py library reflecting the recovered data.
                """
        flag_working = False
        file_name = util.file_name_builder(target, language, date, nult)
        cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cache"))
        path = os.path.join(cache_path, file_name + ".json")
        valid = False
        # check if file exists
        if os.path.isfile(path):
            logger.debug("File exists in cache")
            flag_working = True
            time = pathlib.Path(path).stat().st_mtime
            dt = datetime.datetime.fromtimestamp(time)
            now = datetime.datetime.now()
            ttl = util.get_ttl()

            if (now - dt).total_seconds() > ttl:
                logger.debug("File is older than ttl")
                util.rename_old_file(path)
                valid = False
            else:
                json_data = jsonstatpy.from_file(path)
                valid = True

        if valid is False:
            flag_working, json_data, url = url_build.build_url(target, language, date, nult)
            self.last_url = url
        return flag_working, json_data

    def get_dataframe(self):
        """Returns a dataframe representative of the JSON-stat file through the internal IneJsonStat instance.

                Parameters
                ----------
                self : JsonStatRequest

                Returns
                -------
                A pandas dataframe reflecting the JSON-stat file.
        """
        if self.Ine is not None:
            return self.Ine.get_pandas_dataframe()

    def save_csv(self, file_name):
        """Generates a CSV file representative of the JSON-stat file through the internal IneJsonStat instance.

                Parameters
                ----------
                self : JsonStatRequest
                file_name : string
        """
        if self.Ine is not None:
            self.Ine.save_csv(file_name)

    def generate_dataset(self, json_data):
        """Initializes the IneJsonStat internal attribute and generates the ProcJsonStatDataset object representing
            the JSON-stat file.

            Parameters
            ----------
            self : JsonStatRequest
            json_data : JsonStatDataSet from the jsonstat.py library

            Returns
            -------
            A ProcJsonStatDataset reflecting the JSON-stat file.
        """
        ine = IneJsonStat()
        ine.json_data = json_data
        dataset = ine.generate_object()
        self.Ine = ine
        return dataset

    def query(self, **kwargs):
        """Makes a query with arguments regarding dimensions, status and values in JSON-stat to the main dataset
            and returns the filtered data.

                Parameters
                ----------
                self : JsonStatRequest
                kwargs : Different named arguments regarding dimensions, status and values in JSON-stat
                Returns
                -------
                A pandas dataframe filtered by the query parameters.
        """
        return self.Ine.query(**kwargs)
