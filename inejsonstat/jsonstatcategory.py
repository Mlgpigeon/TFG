# Class that defines the category of a dimension
class JsonStatCategory:
    """
    Class that represents the data of a category in JSON-stat
    """
    def __init__(self, index, label, size):
        self.index = index
        self.label = label
        self.size = size

    def print_properties(self):
        """Prints the name of the properties of a category stored in a JsonStatCategory.

                Parameters
                ----------
                self : JsonStatCategory
        """
        print("Index: ", self.index)
        print("Label: ", self.label)
        print("Size: ", self.size)
