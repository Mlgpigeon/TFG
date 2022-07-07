import pandas as pd

from inejsonstat.dimensionEnum import DimensionEnum
from inejsonstat.dimension_enum_dc import DimensionItem
from inejsonstat.enumerator_hub import EnumeratorHub
from inejsonstat.ine_status import Status
from inejsonstat.jsondataset import ProcJsonStatDataset
from inejsonstat.jsonstatcategory import JsonStatCategory
from inejsonstat.jsonstatdimension import JsonStatDimension
from inejsonstat.jsonutil import JsonUtil as util
from inejsonstat.main_logger import logger


class IneJsonStat:
    """
    Class that manages and generates dynamically the different dimensions and the contained categories based on an
    input JSON-stat file
    """
    def __init__(self):
        self.json_data = None
        self.yaml_data = None
        self.dataset = ProcJsonStatDataset()
        self.log = None
        self.url = None
        self.dimensions_names = []
        self.dimensions_labels = []
        self.dataframe = None
        self.enumerator_hub = None
        self.dimensions_enum = None

    def get_pandas_dataframe(self):
        """Returns a dataframe representative of the JSON-stat file.

                Parameters
                ----------
                self : IneJsonStat

                Returns
                -------
                A pandas dataframe reflecting the JSON-stat file.
        """
        return self.dataframe

    def save_csv(self, file_name):
        """Generates a CSV file representative of the JSON-stat file.

                Parameters
                ----------
                self : IneJsonStat
                file_name : string
        """
        file_name = file_name + ".csv"
        df = self.json_data.to_data_frame()
        df.to_csv(file_name)
        logger.debug("Generated csv: " + file_name)
        print("Generated csv: " + file_name)

    def generate_object(self):
        """Generates a ProcJsonStatDataset correlating to the JSON-stst file, containing the data relative to its
            dimensions and categories.

                Parameters
                ----------
                self : IneJsonStat

                Returns
                -------
                A ProcJsonStatDataset instance with all the data relative to the JSON-stat file in object format
                """
        logger.info("IneJsonStat || Executing module [generate_object]")

        json_data = self.json_data

        self.json_data = json_data
        size = self.get_number_dimensions()

        dataset = ProcJsonStatDataset()
        dimensions = self.generate_dimensions(size)

        for i in range(0, size):
            name = util.normalize_string(dimensions[i].name)
            self.dimensions_names.append(name)
            self.dimensions_labels.append(dimensions[i].label)
            setattr(dataset, name, dimensions[i])

        logger.debug("Dimensions generated")

        value_size, value = self.generate_value()
        setattr(dataset, 'value', value)
        setattr(dataset, 'value_size', value_size)

        status_size, status = self.generate_status()
        setattr(dataset, 'status', status)
        setattr(dataset, 'status_size', status_size)
        setattr(dataset, 'dimension_names', self.dimensions_names)

        self.dataset = dataset
        df = self.json_data.to_data_frame()
        df["Status"] = self.dataset.status
        self.dataframe = df
        self.generate_enumerators()

        return self.dataset

    # Getting the number of dimensions
    def get_number_dimensions(self):
        """Calculates the number of dimensions in a JSON-stat file.

                Parameters
                ----------
                self : IneJsonStat

                Returns
                -------
                Number of dimensions.
        """
        exit_flag = False
        i = 0
        while not exit_flag:
            try:
                self.json_data.dimension(i)
                i = i + 1
            except Exception as e:
                exception_message = 'IneJsonStat || Module [get_number_dimensions], limit position: ' + str(
                    i) + ", " + str(e)
                logger.debug(exception_message)
                exit_flag = True
        return i
        # Generates an index and a label for a dimension category if they exist

    def generate_index(self, dimension, size):
        """Generates 2 dictionaries representing the index and label from a dimension.

                Parameters
                ----------
                self : IneJsonStat
                dimension : JsonStatDimension from the jsonstat.py library
                size : int

                Returns
                -------
                2 dictionaries representing the index and label from a dimension.
        """
        index = dict()
        label = dict()

        has_index = self.check_index(dimension)
        has_label = self.check_label(dimension)

        if has_index:
            for i in range(0, size):
                index[i] = dimension.category(i).index

        if has_label:
            for i in range(0, size):
                label[index[i]] = dimension.category(i).label
        return index, label

        # Generates the category for a dimension

    def generate_category(self, dimension):
        """Generates the categories from a dimension.

                Parameters
                ----------
                self : IneJsonStat
                dimension : JsonStatDimension from the jsonstat.py library

                Returns
                -------
                A category of a JsonStatDimension from the jsonstat.py library.
        """
        size = self.calculate_category_size(dimension)
        logger.info("IneJsonStat || Size of category: " + str(size))
        print("Size of category: ", size)
        index, label = self.generate_index(dimension, size)
        logger.info("IneJsonStat || : " + str(index))
        logger.info("IneJsonStat || Label: " + str(label))
        print("index: ", index)
        print("label: ", label)
        print("size: ", size)
        category = JsonStatCategory(index, label, size)
        return category

        # Generates the dimensions for a dataset

    def generate_dimensions(self, size):
        """Generates the dimensions from a JSON-stat file.

                Parameters
                ----------
                self : IneJsonStat
                size : int

                Returns
                -------
                A list of dimensions JsonStatDimension from the jsonstat.py library.
        """
        dimensions = []
        for i in range(0, size):
            category = self.generate_category(self.json_data.dimension(i))
            role = self.json_data.dimension(i).role
            dimension = JsonStatDimension(self.json_data.dimension(i).did, self.json_data.dimension(i).label,
                                          category, role)
            dimensions.append(dimension)
        return dimensions

        # Getting the size of the category of a given dimension

    @staticmethod
    def get_enum_status(status_in):
        """Gets the value from a Status instance.

                Parameters
                ----------
                status_in : Status

                Returns
                -------
                The value of the given Status.
        """
        status = Status.UNKNOWN
        if status_in == Status.D.name:
            status = Status.D.value
        elif status_in == Status.P.name:
            status = Status.P.value
        elif status_in == Status.E.name:
            status = Status.E.value
        return status

        # Generates the dataset

    def generate_status(self):
        """Generates a list of status from a JSON-stat file.

                Parameters
                ----------
                self : IneJsonStat

                Returns
                -------
                The size of the list and the list.
        """
        exit_flag = False
        status = []
        i = 0
        while not exit_flag:
            try:
                status_value = IneJsonStat.get_enum_status(self.json_data.status(i))
                status.append(status_value)
                i = i + 1
            except Exception as e:
                exception_message = 'IneJsonStat || Module [generate_status], limit position: ' + str(i) + ", " + str(e)
                logger.debug(exception_message)
                exit_flag = True
        return i, status

        # Getting the values of the collection

    def generate_value(self):
        """Generates a list of values from a JSON-stat file.

                Parameters
                ----------
                self : IneJsonStat

                Returns
                -------
                The size of the list and the list.
        """

        exit_flag = False
        value = []
        i = 0
        while not exit_flag:
            try:
                value.append(self.json_data.value(i))
                i = i + 1
            except Exception as e:
                exception_message = 'IneJsonStat || Module [generate_value], limit position: ' + str(i) + ", " + str(e)
                logger.debug(exception_message)
                exit_flag = True

        return i, value

    @staticmethod
    # Getting the size of the category of a given dimension
    def calculate_category_size(dimension):
        """Calculates the size of a category of a dimension.

                Parameters
                ----------
                dimension : JsonStatDimension from the jsonstat.py library

                Returns
                -------
                The size of the category
        """
        exit_flag = False
        i = 0
        while not exit_flag:
            try:
                if dimension.category(i).index is not None:
                    i = i + 1
            except Exception as e:
                exception_message = 'IneJsonStat || Module [calculate_category_size], limit position: ' + str(
                    i) + ", " + str(e)
                logger.debug(exception_message)
                exit_flag = True
        return i

    @staticmethod
    # Checks if the dimension has an index
    def check_index(dimension):
        """Checks if a dimension has an index.

            Parameters
             ----------
            dimension : JsonStatDimension from the jsonstat.py library

            Returns
            -------
            A boolean indicating the existence or lack of.
        """
        flag_index = False
        try:
            index = dimension.category(0).index
            flag_index = True
            if index == '':
                flag_index = False
                print("no index")
        except Exception as e:
            exception_message = 'IneJsonStat || Module [check_index], no index, ' + str(e)
            logger.debug(exception_message)
            print("no index")
        return flag_index

    @staticmethod
    # Checks if the dimension has a label
    def check_label(dimension):
        """Checks if a dimension has a label.

                Parameters
                ----------
                dimension : JsonStatDimension from the jsonstat.py library

                Returns
                -------
                A boolean indicating the existence or lack of.
        """
        logger.info("IneJsonStat || Executing module [check_label]")
        flag_label = False
        try:
            label = dimension.category(0).label
            flag_label = True
            if label == '':
                flag_label = False
                print("no label")
        except Exception as e:
            exception_message = 'IneJsonStat || Module [check_label], no label, ' + str(e)
            logger.debug(exception_message)
            print("no label")
        return flag_label

    def generate_enumerators(self):
        """Generates enumerators corresponding to dimensions as EnumeratorHub and its label values as DimensionEnum.

                Parameters
                ----------
                self : IneJsonStat

        """
        table = self.dataframe
        enums = []
        dimension_dictionary = {}
        dictionary_enumerator = {}

        for a in self.dimensions_names:
            dimension = getattr(self.dataset, a)
            category = getattr(dimension, 'category')
            dimension_label = getattr(dimension, 'label')
            label = getattr(category, 'label')
            values = list(label.values())
            dimension_enum_name = util.normalize_enum(a)

            dictionary = {}
            for value in values:
                adapted_name = util.normalize_enum(value)

                filtered_table = table.loc[table[dimension_label] == value]
                #filtered_table = filtered_table.dropna()
                table2 = table[table.isin([value]).any(axis=1)].dropna()
                indextable = table2.index.tolist()
                statustable = []

                for i in indextable:
                    statustable.append(self.dataset.status[i])

                table2["Status"] = statustable
                del table2[dimension_label]

                statustable = table2.drop(columns=["Value"])
                status_list = statustable.values

                valuetable = table2.drop(columns=["Status"])
                value_list = valuetable.values

                data_list = table2.values

                adapted_name = util.check_repeated(adapted_name, enums)
                enums.append(adapted_name)

                tuplenamed = DimensionItem(adapted_name, value, table2.columns.values, table2, valuetable, statustable,
                                           data_list, value_list, status_list)
                dictionary[adapted_name] = tuplenamed

            enumerator = DimensionEnum('DynamicEnum', dictionary)

            dictionary_enumerator[dimension_enum_name] = enumerator
            dimension_dictionary[dimension_enum_name] = a
        enumerator_dimensions = EnumeratorHub('DynamicEnum', dimension_dictionary)

        self.enumerator_hub = enumerator_dimensions
        self.dimensions_enum = dictionary_enumerator

        print("Lista de enumeradores ", self.dimensions_enum.keys())
        for a in self.dimensions_enum.keys():
            setattr(self.dataset, a, self.dimensions_enum[a])
        setattr(self.dataset, "enumerator_hub", self.enumerator_hub)

    def query(self, **kwargs):
        """Makes a query with arguments regarding dimensions, status and values in JSON-stat to the main dataset
            and returns the filtered data.

                Parameters
                ----------
                self : IneJsonStat
                kwargs : Different named arguments regarding dimensions, status and values in JSON-stat
                Returns
                -------
                A pandas dataframe filtered by the query parameters.
        """
        columns = self.dimensions_labels + ["Status", "Value"]
        query_values = []
        for arg_l in kwargs:
            if arg_l in self.dimensions_names:
                if isinstance(kwargs[arg_l], list):
                    for arg in kwargs[arg_l]:
                        if str(arg) in self.dimensions_enum[str(arg_l).upper()].list_labels():
                            column = getattr(self.dataset, arg_l).label
                            query_values.append([column, str(arg)])
                        else:
                            print("Invalid dimension value")
                else:
                    string_aux = util.normalize_string(str(kwargs[arg_l]))
                    string3 = str(getattr(self.dataset, arg_l).label)
                    if string_aux == "no":

                        columns.remove(string3)

                    elif str(kwargs[arg_l]) in self.dimensions_enum[str(arg_l).upper()].list_labels():
                        query_values.append([string3, str(kwargs[arg_l])])

                    else:
                        print("Invalid dimension value")

            elif arg_l == "values":
                string = util.normalize_string(str(kwargs[arg_l]))
                if string == "no":
                    columns.remove("Value")
            elif arg_l == "status":
                string = util.normalize_string(str(kwargs[arg_l]))
                if string == "no":
                    columns.remove("Status")

        df = self.dataframe[columns]
        list_aux = []
        if len(query_values) > 0:
            for i in query_values:

                df2 = df.loc[df[i[0]] == i[1]]
                list_aux.append(df2)
            df_out = pd.concat(list_aux, join="inner")
        else:
            df_out = df

        return df_out
