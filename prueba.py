from data_model.ine_initializer import IneInitializer as ine_init


def print_data(dataset, enums):
    print("")
    print("Object : ", dataset.comunidadesautonomasyprovincias.name, "-------------------------")
    print("Role:", dataset.comunidadesautonomasyprovincias.role)
    print("Index: ", dataset.comunidadesautonomasyprovincias.category.index)
    print("Label:", dataset.comunidadesautonomasyprovincias.category.label)
    print("Size : ", dataset.comunidadesautonomasyprovincias.category.size)
    print("")

    print("Object : ", dataset.per.name, "-------------------------")
    print("Role: ", dataset.per.role)
    print("Index: ", dataset.per.category.index)
    print("Label:", dataset.per.category.label)
    print("Size : ", dataset.per.category.size)
    print("")

    print("Dimensions: ", dataset.dimensions)
    print("Value: ", dataset.value)
    print("Status: ", dataset.status)
    print("Status size: ", dataset.status_size)
    print("")
    dataset.printed_dimensions()
    print("Values of Badajoz =", enums.BADAJOZ.values("periodo"))
    print(enums.BADAJOZ.values_df)
    print(enums.BADAJOZ.columns)
    #resultado.query("comunidadesyprovincias = enums.BADAJOZ")
    #print("Status of N2021M10 = ", enums.N2021M10.status)
    #print(enums.BADAJOZ.data('2021m12'))
    #print(enums.N2021M12.values('baDaJoz'))
    #print(enums.N2021M12.values(1.82))
    #print(enums.N2021M12.values('baDaJoz', 1.82))
    #print(enums.N2021M12.data('baDaJoz', 1.82))
    #print(enums.N2021M12.columns)
    #print(enums.N2021M12.dataframe)

def print_data2(dataset):
    print("")
    print("Object : ", dataset.comunidadesautonomasyprovincias.name, "-------------------------")
    print("Role:", dataset.comunidadesautonomasyprovincias.role)
    print("Index: ", dataset.comunidadesautonomasyprovincias.category.index)
    print("Label:", dataset.comunidadesautonomasyprovincias.category.label)
    print("Size : ", dataset.comunidadesautonomasyprovincias.category.size)
    print("")

    print("Object : ", dataset.per.name, "-------------------------")
    print("Role: ", dataset.per.role)
    print("Index: ", dataset.per.category.index)
    print("Label:", dataset.per.category.label)
    print("Size : ", dataset.per.category.size)
    print("")

    print("Object : ", dataset.n7.name, "-------------------------")
    print("Role: ", dataset.n7.role)
    print("Index: ", dataset.n7.category.index)
    print("Label:", dataset.n7.category.label)
    print("Size : ", dataset.n7.category.size)
    print("")

    print("Object : ", dataset.residencia.name, "-------------------------")
    print("Role: ", dataset.residencia.role)
    print("Index: ", dataset.residencia.category.index)
    print("Label:", dataset.residencia.category.label)
    print("Size : ", dataset.residencia.category.size)
    print("")


# main function
if __name__ == "__main__":
    ine = ine_init.create("config.yaml")

    generated_dataset = ine.get_dataset()


    #df = ine.get_pandas_dataframe()
    #print(df)
    #df.to_csv("data.csv")

    generated_dataset.printed_dimensions()
    #print(enums.__members__.keys())

    #print_data(generated_dataset, enums)

    enums = ine_init.get_value1(ine)
    #print_data(generated_dataset,enums)