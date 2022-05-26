import enum
from dataclasses import dataclass
from data_model.ine_status import Status
from collections import namedtuple

DimensionItem = namedtuple("DimensionItem",["id","name", "columns", "dataframe","values_df","status_df", "data", "values", "status"])