from config import cursor
import utils


def ObtenerCamposAlumno(numeroalumno):
    with cursor:
        # ? TABLA ALUMNOS_CXC
        cursor.execute(
            f"SELECT NUMEROALUMNO, PAGADO FROM ALUMNOS_CXC WHERE NUMEROALUMNO='{numeroalumno}'"
        )

        headersCxc = utils.FirebirdGetHeaders(cursor.description)
        valuesCxc = utils.MergeHeadersValues(headersCxc, cursor.fetchall())

        # ? TABLA ALUMNOS
        cursor.execute(
            f"SELECT NUMEROALUMNO, NOMBRE, PATERNO, MATERNO, NIVEL FROM ALUMNOS WHERE NUMEROALUMNO='{numeroalumno}'"
        )

        headersAlumno = utils.FirebirdGetHeaders(cursor.description)
        valuesAlumno = utils.MergeHeadersValues(headersAlumno, cursor.fetchall())

        # MERGED
        merged = utils.MergedListsOfDicts(valuesCxc, valuesAlumno, "numeroalumno")

        return merged
