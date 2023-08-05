from flask import Blueprint
import controllers.datafields_controllers as Controller
from flask_cors import cross_origin

datafieldsRoutes = Blueprint("datafields", __name__, url_prefix="/datafields")


@datafieldsRoutes.route("/", methods=["GET"])
@cross_origin()
def CargarDataFields():
    return Controller.CargarDataFields()


@datafieldsRoutes.route("/ciclos", methods=["GET"])
@cross_origin()
def CargarCiclos():
    return Controller.CargarCiclos()


@datafieldsRoutes.route("/carreras/<periodo>", methods=["GET"])
@cross_origin()
def CargarCarreras(periodo):
    return Controller.CargarCarreras(periodo)


@datafieldsRoutes.route("/grupos/<periodo>/<nivel>", methods=["GET"])
@cross_origin()
def CargarGrupos(periodo, nivel):
    return Controller.CargarGrupos(periodo, nivel)


@datafieldsRoutes.route("/meses", methods=["GET"])
@cross_origin()
def CargarMeses():
    return Controller.CargarMeses()
