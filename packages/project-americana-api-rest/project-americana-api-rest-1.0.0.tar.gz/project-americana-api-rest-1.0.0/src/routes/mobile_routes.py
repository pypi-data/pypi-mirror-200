from flask import Blueprint
from flask_cors import cross_origin
import controllers.mobile_controllers as Controller

mobileRoutes = Blueprint("mobile", __name__, url_prefix="/mobile")


@mobileRoutes.route("/<numeroalumno>", methods=["GET"])
@cross_origin()
def ObtenerCamposAlumno(numeroalumno):
    return Controller.ObtenerCamposAlumno(numeroalumno)
