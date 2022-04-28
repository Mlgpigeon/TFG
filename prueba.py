import inejsonstat as inejsonstat


def print_data(dataset):
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
    print("")

    dataset.printed_dimensions()


# main function
if __name__ == "__main__":
    ine = inejsonstat.IneJsonStat()
    ine.create()

    generated_dataset = ine.get_dataset()
    print_data(generated_dataset)
