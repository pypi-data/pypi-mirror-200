from flask import Blueprint
from flask_cors import cross_origin
import controllers.recibos_controllers as Controller

recibosRoutes = Blueprint("recibos", __name__, url_prefix="/recibos")


@recibosRoutes.route("/<nivel>/<codigogrupo>/<periodo>/<mes>", methods=["GET"])
@cross_origin()
def GenerarTickets(nivel, codigogrupo, periodo, mes):
    return Controller.GenerarTicket(nivel, codigogrupo, periodo, mes)
