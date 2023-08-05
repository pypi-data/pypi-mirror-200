from config import cursor
import utils


def GenerarTickets(nivel, codigogrupo, periodo, mes):
    with cursor:
        cursor.execute(
            f"""SELECT
                    ALUMNOS_CXC.NUMEROALUMNO, 
                    ALUMNOS_CXC.REFERENCIA,  
                    ALUMNOS_CXC.CANTIDADPROGRAMADA, 
                    ALUMNOS_CXC.REFERENCIA2, 
                    ALUMNOS_CXC.MES,
                    ALUMNOS_GRUPOS.CODIGOGRUPO, 
                    ALUMNOS_GRUPOS.PERIODO, 
                    ALUMNOS.NOMBRE, 
                    ALUMNOS.MATERNO, 
                    ALUMNOS.PATERNO,
                    ALUMNOS.NIVEL,
                    ALUMNOS.CORREO_INSTITUCIONAL
                FROM (
                    (ALUMNOS_CXC INNER JOIN ALUMNOS_GRUPOS ON ALUMNOS_CXC.NUMEROALUMNO = ALUMNOS_GRUPOS.NUMEROALUMNO)
                        INNER JOIN ALUMNOS ON ALUMNOS_CXC.NUMEROALUMNO = ALUMNOS.NUMEROALUMNO)
                    WHERE ALUMNOS_GRUPOS.CODIGOGRUPO= '{codigogrupo}'
                    AND ALUMNOS.NIVEL = '{nivel}'
                    AND ALUMNOS_GRUPOS.PERIODO= {periodo}
                    AND ALUMNOS_CXC.PERIODO= {periodo}
                    AND ALUMNOS_CXC.MES = {mes} """
        )

        listHeaders = []
        listValues = []

        listHeaders = utils.FirebirdGetHeaders(cursor.description)
        listValues = utils.MergeHeadersValues(listHeaders, cursor.fetchall())

        cursor.execute(
            f"""SELECT 
                            SUBSTRING(CFGPAGOS_DET.PERIODO_INICIO FROM 1 FOR 10) AS PAGO_PRONTO,
                            SUBSTRING(CFGPAGOS_DET.PERIODO_FINAL FROM 1 FOR 10) AS PAGO_ATRASADO
                        FROM CFGPAGOS_DET 
                            WHERE CFGPAGOS_DET.PERIODO = {periodo} 
                            AND CFGPAGOS_DET.NIVEL = '{nivel}' 
                            AND CFGPAGOS_DET.MES = {mes} """
        )

        listHeadersPagos = []
        listValuesPagos = []

        listHeadersPagos = utils.FirebirdGetHeaders(cursor.description)
        listValuesPagos = utils.MergeHeadersValues(listHeadersPagos, cursor.fetchall())

        # print(listValuesPagos)

        listMergedValues = []

        for alumno in listValues:
            for fecha in listValuesPagos:
                listMergedValues.append(alumno | fecha)

        # print(listMergedValues)

        return listMergedValues


""" 
def GenerarTickets(nivel, codigogrupo, periodo, mes):
    with cursor:

        # ? TABLA ALUMNOS
        cursor.execute(
            f"SELECT NUMEROALUMNO, NOMBRE, MATERNO, PATERNO FROM ALUMNOS WHERE NIVEL='{nivel}'"
        )
        headersAlumnos = []
        valuesAlumnos = []

        for item in cursor.description:
            headersAlumnos.append(item[0].lower())

        resultadoCursor = cursor.fetchall()
        if not resultadoCursor:
            return []
        for item in resultadoCursor:
            dic = {}
            for indice, valor in enumerate(item):
                dic[headersAlumnos[indice]] = valor
            valuesAlumnos.append(dic)

        # ? TABLA ALUMNOS_GRUPOS
        cursor.execute(
            f"SELECT NUMEROALUMNO, CODIGOGRUPO, PERIODO FROM ALUMNOS_GRUPOS WHERE CODIGOGRUPO='{codigogrupo}' AND PERIODO='{periodo}'"
        )
        headersAlumnosGrupos = []
        valuesAlumnosGrupos = []

        for item in cursor.description:
            headersAlumnosGrupos.append(item[0].lower())

        resultadoCursor = cursor.fetchall()
        if not resultadoCursor:
            return []
        for item in resultadoCursor:
            dic = {}
            for indice, valor in enumerate(item):
                dic[headersAlumnosGrupos[indice]] = valor
            valuesAlumnosGrupos.append(dic)

        # ? TABLA ALUMNOS_CXC
        cursor.execute(
            f"SELECT NUMEROALUMNO, REFERENCIA, FECHA_SP1, CANTIDADPROGRAMADA, REFERENCIA2, FECHA_SP2, MES FROM ALUMNOS_CXC WHERE MES ='{mes}' AND PERIODO='{periodo}'"
        )
        headersAlumnosCxc = []
        valuesAlumnosCxc = []

        for item in cursor.description:
            headersAlumnosCxc.append(item[0].lower())

        resultadoCursor = cursor.fetchall()
        if not resultadoCursor:
            return []
        for item in resultadoCursor:
            dic = {}
            for indice, valor in enumerate(item):
                dic[headersAlumnosCxc[indice]] = valor
            valuesAlumnosCxc.append(dic)

        # ? MERGES
        # * merged alumnos - alumnos_grupos
        mergedValues = []
        for item in valuesAlumnos:
            try:
                filtro = next(
                    alumno
                    for alumno in valuesAlumnosGrupos
                    if alumno["numeroalumno"] == item["numeroalumno"]
                )
                mergedValues.append(item | filtro)
            except StopIteration:
                pass

        if not mergedValues:
            return []

        # * merged alumnos-alumnos_grupos - alumnos_cxc
        ticketsValues = []
        for item in mergedValues:
            try:
                filtro = next(
                    alumno
                    for alumno in valuesAlumnosCxc
                    if alumno["numeroalumno"] == item["numeroalumno"]
                )
                ticketsValues.append(item | filtro)
            except StopIteration:
                pass

    return ticketsValues
 """
