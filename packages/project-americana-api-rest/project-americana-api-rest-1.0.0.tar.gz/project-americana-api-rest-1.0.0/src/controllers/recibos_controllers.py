from flask import jsonify
import models.recibos_models as Model


def GenerarTicket(nivel, codigogrupo, periodo, mes):
    return jsonify(Model.GenerarTickets(nivel, codigogrupo, periodo, mes))
