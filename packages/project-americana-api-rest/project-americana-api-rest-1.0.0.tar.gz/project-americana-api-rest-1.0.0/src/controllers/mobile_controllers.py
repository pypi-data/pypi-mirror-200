from flask import jsonify
from models import mobile_models as Model


def ObtenerCamposAlumno(numeroalumno):
    return jsonify(Model.ObtenerCamposAlumno(numeroalumno))
