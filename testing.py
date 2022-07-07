import datetime

import inejsonstat.__init__ as ine_init

if __name__ == "__main__":
    date = datetime.date(year=2021, month=5, day=1)
    date2 = datetime.date(year=2021, month=4, day=1)
    date3 = datetime.date(year=2021, month=3, day=1)
    date4 = datetime.date(year=2023, month=3, day=1)

    # Initialize the program
    ine = ine_init.create()

    # Example with written date and language
    json_data = ine.do_request(target='2065', language='ES', date=date, datetype="range")
    dataset = ine.generate_dataset(json_data)
    df = ine.get_dataframe()
    print(df)

    print("From the url:", ine.last_url)
    json_data = ine.do_request(target=ine.targets.N2065, language=ine.languages.EN, date="20210501:20210601")

    print("From the url:", ine.last_url)

    # Example of ranged date
    ine.do_request(target=ine.targets.N2065, language=ine.languages.EN, date=[date, date2], datetype="range", nult=2)
    print("From the url:", ine.last_url)

    # Main example
    # Get the json_stat data
    print("[1]-----------------------------------------------------------------------------")
    json_data = ine.do_request(target=ine.targets.N2074, language=ine.languages.ES, date=[date, date2, date3],
                               datetype="list")
    print("The Json data is:")
    print(json_data)
    print("From the url:", ine.last_url)

    # Initialize dataset
    print("[2]-----------------------------------------------------------------------------")
    dataset = ine.generate_dataset(json_data)

    # Get the dataframe
    print("[3]-----------------------------------------------------------------------------")
    df = ine.get_dataframe()
    print("The dataframe is:")
    print(df)

    # Save as csv
    print("[4]-----------------------------------------------------------------------------")
    ine.save_csv("example")

    print("[5]-----------------------------------------------------------------------------")
    print("Dataset dimensions are: ", dataset.dimensions)
    print("Dimensión:", dataset.comunidadesautonomasyprovincias)
    print("Dimensión>category>label:", dataset.comunidadesautonomasyprovincias.category.label)
    dataset.comunidadesautonomasyprovincias.print_properties()
    dataset.comunidadesautonomasyprovincias.category.print_properties()

    print("[6]-----------------------------------------------------------------------------")
    print("Dataset attributes: ")
    dataset.print_attributes()

    print("[7]-----------------------------------------------------------------------------")
    print("Dataset value list:", len(dataset.value))
    print("Size of value list: ", dataset.value_size)

    print("[8]-----------------------------------------------------------------------------")
    print("Dataset status list:", len(dataset.status))
    print("Size of status list: ", dataset.status_size)

    print("[9]-----------------------------------------------------------------------------")
    print("For any dimension in the dataset:")
    dataset.n7.print_properties()

    print("[10]-----------------------------------------------------------------------------")
    print("Enumerators are:", dataset.enumerator_hub.list())

    print("[11]-----------------------------------------------------------------------------")
    print("Example of dimension enumerator members is :",
          dataset.COMUNIDADESAUTONOMASYPROVINCIAS.list())

    print("[12]-----------------------------------------------------------------------------")
    print("Column list related to a given enumerator members: ")
    print(dataset.COMUNIDADESAUTONOMASYPROVINCIAS.BADAJOZ.columns)

    print("[13]-----------------------------------------------------------------------------")
    print("Data dataframe related to a given enumerator member: ")
    print(dataset.COMUNIDADESAUTONOMASYPROVINCIAS.BADAJOZ.data_df())

    print("[14]-----------------------------------------------------------------------------")
    print("Value dataframe related to a given enumerator member: ")
    print(dataset.COMUNIDADESAUTONOMASYPROVINCIAS.BADAJOZ.values_df())

    print("[15]-----------------------------------------------------------------------------")
    print("Status dataframe related to a given enumerator member: ")
    print(dataset.COMUNIDADESAUTONOMASYPROVINCIAS.BADAJOZ.status_df())

    print("[16]-----------------------------------------------------------------------------")
    # Queries can be called with enums or strings as parameters
    df1 = ine.query(comunidadesautonomasyprovincias=dataset.COMUNIDADESAUTONOMASYPROVINCIAS.BADAJOZ)
    df2 = ine.query(comunidadesautonomasyprovincias="Badajoz")

    print(df1)
    print(df2)

    print("[17]-----------------------------------------------------------------------------")
    # Columns can be deactivated on the result
    df3 = ine.query(comunidadesautonomasyprovincias="no", status="NO")
    print(df3)

    print("[18]-----------------------------------------------------------------------------")
    # There can be multiple values for a query
    df4 = ine.query(comunidadesautonomasyprovincias=[dataset.COMUNIDADESAUTONOMASYPROVINCIAS.BADAJOZ,
                                                     "Granada"], status="NO")
    print(df4)
