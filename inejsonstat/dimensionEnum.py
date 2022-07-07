from enum import Enum


class DimensionEnum(Enum):
    """
    Enumerator that represents a category value of a dimension in the JSON-stat standard.
    """

    def __str__(self):
        """Overwrites the __str__ default method to output the name value

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                The name value as a string
        """
        return str(self.value.name)

    @classmethod
    def list_labels(cls):
        """Creates a list with the name values of every Enumerator DimensionEnum in the object

                Parameters
                ----------
                cls : DimensionEnum class

                Returns
                -------
                The list of the mapped name values
        """
        return list(map(lambda c: c.value.name, cls))

    @classmethod
    def list(cls):
        """Creates a list with the names of every Enumerator DimensionEnum in the object

                Parameters
                ----------
                cls : DimensionEnum class

                Returns
                -------
                The list of the mapped name values
        """
        return list(map(lambda c: c.name, cls))

    @property
    def label(self):
        """Returns the name value of a DimensionEnum, which correlates to a label value in a JSON-stat category.

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                The name of the DimensionEnum, generally as a string
        """
        return self.value.name

    @property
    def values(self):
        """Returns the list of values related to a label value in a JSON-stat category.

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                List of values, generally numeric in nature
        """
        return self.value.values

    def values_df(self):
        """Returns a dataframe with a values column related to a label value in a JSON-stat category.

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                A pandas dataframe reflecting the values related to a category's label.
        """
        return self.value.values_df

    @property
    def columns(self):
        """Returns the name value of a DimensionEnum, which correlates to a label value in JSON-stat category.

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                The name of the DimensionEnum, generally as a string
        """
        return self.value.columns

    def data_df(self):
        """Returns a dataframe with a values and status columns related to a label value in a JSON-stat category.

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                A pandas dataframe reflecting the values and status related to a category's label.
        """
        return self.value.dataframe

    @property
    def status(self):
        """Returns the list of status related to a label value in a JSON-stat category.

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                List of status
                """
        return self.value.status

    def status_df(self):
        """Returns a dataframe with a status column related to a label value in a JSON-stat category.

                Parameters
                ----------
                self : DimensionEnum

                Returns
                -------
                A pandas dataframe reflecting the status related to a category's label.
        """
        return self.value.status_df
