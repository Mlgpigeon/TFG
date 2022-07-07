from collections import namedtuple
"""A named tuple used internally to store the different values of a dimension
"""
DimensionItem = namedtuple("DimensionItem",  ["id", "name", "columns", "dataframe", "values_df", "status_df", "data",
                                              "values", "status"])
