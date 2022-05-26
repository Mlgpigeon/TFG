from data_model.ine_initializer import IneInitializer as ine_init

# main function
if __name__ == "__main__":

    # Para empezar se crea un objeto de la clase IneInitializer con el fichero de configuración yaml deseado
    # Con esto se prueba la url y se crean los valores en base al json
    ine = ine_init.create("config.yaml")

    # Opción 1

    ine.dataset = Dataset.Pernotaciones  # "2074" Definido manualmente (de momento)
    ine.date = Date(year=2021, month=5, day=21)
    ine.language = Languages.Spanish  # "ES" Definido manualmente (de momento)
    ine.items = 4

    ine.do_request()
        # do_request date_as_string = self.date_to_string("YYYYMMDD")

    # Opción 2

    ine.do_request(
        dataset=Dataset.Pernotaciones,
        date=Date(year=2021, month=5, day=21),
        language=Languages.Spanish,
        items=4
    )

    # Opción 3

    ine.dataset = Dataset.Pernotaciones  # "2074" Definido manualmente (de momento)
    ine.language = Languages.Spanish  # "ES" Definido manualmente (de momento)
    ine.items = 4

    ine.do_request(date=Date(year=2021, month=5, day=21))

    # Proceso los datos de esta petición

    ine.do_request(date=Date(year=2021, month=5, day=22))

    # Proceso los nuevos datos, los anteriores los sobreescribo

    ine.do_request(date=Date(year=2021, month=5, day=23))

    # Idem



    # El objeto IneInitializer tiene un objeto interno dataset creado de tipo IneDataset que puede obtenerse

    generated_dataset = ine.get_dataset()

    print("[1]-----------------------------------------------------------------------------")
    print("Las dimensiones del dataset son: ", generated_dataset.dimension_list)

    print("[2]-----------------------------------------------------------------------------")
    print("Para conocer los atributos llamables del dataset: ")
    generated_dataset.print_callables()

    print("[3]-----------------------------------------------------------------------------")
    print("Lista de valores del dataset:", generated_dataset.value)
    print("Tamaño de la lista de valores: ", generated_dataset.value_size)

    print("[4]-----------------------------------------------------------------------------")
    print("Lista de status del dataset:", generated_dataset.status)
    print("Tamaño de la lista de status: ", generated_dataset.status_size)

    print("[5]-----------------------------------------------------------------------------")
    print("Para cualquier dimensión en el dataset:")
    generated_dataset.n7.print_properties()

    print("[6]-----------------------------------------------------------------------------")
    # Obtener el dataset como dataframe de pandas
    df = ine.get_pandas_dataframe()
    print("El dataframe en pandas es:")
    print(df)

    print("[7]-----------------------------------------------------------------------------")
    ine.get_csv(file_name="excel")

    print("[8]-----------------------------------------------------------------------------")
    # Generate enumerators
    enumerators, dimensions = ine.generate_enumerators()
    print(type(enumerators))
    print(type(dimensions))

    print("[9]-----------------------------------------------------------------------------")
    print("Dimensiones para el mapa de enumeradores:", dimensions.list())

    print("[10]-----------------------------------------------------------------------------")
    print("Lista de enumeradores:", enumerators.keys())

    print("[11]-----------------------------------------------------------------------------")
    print("Lista de miembros por enumerador: ", enumerators[str(dimensions.COMUNIDADESAUTONOMASYPROVINCIAS)].list())

    comunidadesautonomasyprovincias = enumerators[str(dimensions.COMUNIDADESAUTONOMASYPROVINCIAS)]

    print("[12]-----------------------------------------------------------------------------")
    print("Lista de columnas relacionadas con un valor de enumeración concreto: ")
    print(comunidadesautonomasyprovincias.BADAJOZ.columns)

    print("[13]-----------------------------------------------------------------------------")
    print("Lista de valores relacionados con un valor de enumeración concreto: ")
    print(comunidadesautonomasyprovincias.BADAJOZ.data_df())

    print("[14]-----------------------------------------------------------------------------")
    print("Lista de values relacionados con un valor de enumeración concreto: ")
    print(comunidadesautonomasyprovincias.BADAJOZ.values_df())

    print("[15]-----------------------------------------------------------------------------")
    print("Lista de status relacionados con un valor de enumeración concreto: ")
    print(comunidadesautonomasyprovincias.BADAJOZ.status_df())

    print("[16]-----------------------------------------------------------------------------")
    # Las queries pueden llamarse con enumeradores o con labels
    df1 = ine.query(comunidadesautonomasyprovincias=comunidadesautonomasyprovincias.BADAJOZ)
    df2 = ine.query(comunidadesautonomasyprovincias="Badajoz")

    print(df1)
    print(df2)

    print("[17]-----------------------------------------------------------------------------")
    # Pueden desactivarse columnas
    df3 = ine.query(comunidadesautonomasyprovincias="no",status="NO")
    print(df3)

    print("[18]-----------------------------------------------------------------------------")
    # Pueden darse varios colores por columnas
    df4 = ine.query(comunidadesautonomasyprovincias=[comunidadesautonomasyprovincias.BADAJOZ,
                                                     comunidadesautonomasyprovincias.GRANADA], status="NO")
    print(df4)

    # ----
