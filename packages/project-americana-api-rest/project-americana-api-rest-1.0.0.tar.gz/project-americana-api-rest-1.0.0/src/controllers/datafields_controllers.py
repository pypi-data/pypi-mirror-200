from flask import jsonify
import models.datafields_models as Model


def CargarDataFields():
    return jsonify(Model.CargarDataFields())


def CargarCiclos():
    return jsonify(Model.CargarCiclos())


def CargarCarreras(periodo):
    return jsonify(Model.CargarCarreras(periodo))


def CargarGrupos(periodo, nivel):
    return jsonify(Model.CargarGrupos(periodo, nivel))


def CargarMeses():
    return jsonify(Model.CargarMeses())
