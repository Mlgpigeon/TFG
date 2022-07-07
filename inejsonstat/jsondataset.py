
class ProcJsonStatDataset:
    """
    Class that stores all data from a JSON-stat file once converted to objects dynamically.
    """
    def __init__(self):
        self.name = 'dataset'
        self.dimension_names = None

    @property
    def dimensions(self):
        """Returns a list of the names of the dimensions in a ProcJsonStatDataset.

                Parameters
                ----------
                self : ProcJsonStatDataset

                Returns
                -------
                A list of the names of the dimensions in string format.
        """
        return self.dimension_names

    # Returns a list of dimensions in the dataset
    @property
    def attributes(self):
        """Returns the attributes of the instance of ProcJsonStatDataset.

                Parameters
                ----------
                self : ProcJsonStatDataset

                Returns
                -------
                The items of the dict of attributes of the instance.
        """
        return self.__dict__.items()

    # Print all dimensions of the dataset
    def print_attributes(self):
        """Prints the attributes of the instance of ProcJsonStatDataset.
                Parameters
                ----------
                self : ProcJsonStatDataset
        """
        print("Attributes of dataset: ")
        for key, value in self.attributes:
            print(key)
