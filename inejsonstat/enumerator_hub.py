from aenum import Enum


class EnumeratorHub(Enum):
    """
    Enumerator that represents a dimension in JSON-stat and contains DimensionEnums dynamically representing its labels
    """

    def __str__(self):
        """Overwrites the __str__ default method to output the value

                Parameters
                ----------
                self : EnumeratorHub

                Returns
                -------
                The value of the EnumeratorHub
        """
        return str(self.value)

    @classmethod
    def list(cls):
        """Creates a list with the names of every Enumerator EnumeratorHub in the object

                Parameters
                ----------
                cls : DimensionEnum class

                Returns
                -------
                The list of the mapped name
        """
        return list(map(lambda c: c.name, cls))

    @classmethod
    def list_labels(cls):
        """Creates a list with the values of every Enumerator DimensionEnum in the object

                Parameters
                ----------
                cls : DimensionEnum class

                Returns
                -------
                The list of the mapped values
        """
        return list(map(lambda c: c.value, cls))
