from inejsonstat.jsonstatrequest import JsonStatRequest
from inejsonstat.jsonutil import JsonUtil as util
from inejsonstat.languages_enum import LanguageEnum
from inejsonstat.main_logger import logger
from inejsonstat.target_enum import TargetEnum

"""
Initializes the library by creating request objects as instances of JsonStatRequest
"""


def create(target=None, language=None, date: str = None, datetype: str = None, nult=None):
    """Returns a dataframe representative of the JSON-stat file.

            Parameters
            ----------
            target : string or TargetEnum
            language : string or LanguageEnum
            date : string or date from datetime
            datetype : string
            nult  : string or int

            Returns
            -------
            A JsonStatRequest with the not None parameters initialized internally.
    """
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

    nult_in = None
    if nult is not None:
        if type(nult) is int:
            nult_in = nult
        elif type(nult) is str:
            if util.check_int(nult):
                nult_in = nult
            else:
                raise Exception("nult is not an integer")

    request = JsonStatRequest(target_in, language_in, date_in, nult_in)

    return request
