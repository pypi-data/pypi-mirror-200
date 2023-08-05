def MergeHeadersValues(listHeaders: list, listValues: list) -> list:
    """Combina una lista de encabezados y una lista de tuples con valores

    Esta función combina una lista de llaves y una lista de tuples con valores en una lista de  diccionarios

    Args:
        listHeaders (list) : Lista de los encabezados en formato string
            ['nombre','apellido','edad']
        listValues (list) : Lista de los valores en tuples
            [('Mauricio','Maya',25),('Raquel','Ruiz',34), ...]

    Returns:
        list : Lista de diccionarios a partir de las llaves y valor
    """

    # cursor.description > (('ID', <class 'int'>), ('NOMBRE', <class 'str'>))
    # cursor.fetchall > [('C', 1972), ('Python', 1991)]

    mergedList = []
    for item in listValues:
        dic = {}
        for indice, valor in enumerate(item):
            dic[listHeaders[indice]] = valor
        mergedList.append(dict(sorted(dic.items())))
    return mergedList


def MergedListsOfDicts(listOne: list, listTwo: list, key: str) -> list:
    """Combina dos listas de diccionarios a partir de una key dada

    Toma cada item de listOne y compara la llave data con las llaves en los diccionarios de listTwo, si la llave coincide combina los diccionarios

    Args:
        listOne (list) : Lista de diccionarios de la cual se va tomar cada item
        listTwo (list) : Lista de diccionarios en la que se va a comparar la llave
        key (str) : Llave de diccionario con la que se va a hacer match en los diccionarios

    Returns:
        list : Lista de diccionarios que contiene los diccionarios que coinciden
    """

    """ 
        alum = list(
            filter(lambda per: per["NUMEROALUMNO"] == 10230, resultadoAlumnosGrupos)
        )
        print(alum) # ==> [{'INICIAL': 2020, 'FINAL': 2021, 'NUMEROALUMNO': 10230}, {'INICIAL': 2020, 'FINAL': 2021, 'NUMEROALUMNO': 10230}, {'INICIAL': 2021, 'FINAL': 2021, 'NUMEROALUMNO': 10230}, {'INICIAL': 2022, 'FINAL': 2022, 'NUMEROALUMNO': 10230}, {'INICIAL': 2022, 'FINAL': 2022, 'NUMEROALUMNO': 10230}, {'INICIAL': 2022, 'FINAL': 2022, 'NUMEROALUMNO': 10230}]

        alum = next(
            item for item in resultadoAlumnosGrupos if item["NUMEROALUMNO"] == 10230
        )
        print(alum)  # ==> {'INICIAL': 2020, 'FINAL': 2021, 'NUMEROALUMNO': 10230} """

    mergedList = []
    for item in listOne:
        try:
            filtro = next(dic for dic in listTwo if dic[key] == item[key])
            temp = item | filtro
            if temp not in mergedList:
                mergedList.append(temp)
        except StopIteration:
            pass
    return mergedList


def FirebirdGetHeaders(cursorDescription: tuple) -> list:
    """Obtiene los header del cursor.description de firebird"""

    # cursor.description > (('ID', <class 'int'>), ('NOMBRE', <class 'str'>))
    # cursor.fetchall > [('C', 1972), ('Python', 1991)]

    listHeaders = []
    for item in cursorDescription:
        listHeaders.append(item[0].lower())
    return listHeaders


def FirebirdFilterDuplicates(listDuplicates: list) -> list:
    resultado = []
    for item in listDuplicates:
        if item[0] not in resultado:
            resultado.append(item[0])
    return resultado
