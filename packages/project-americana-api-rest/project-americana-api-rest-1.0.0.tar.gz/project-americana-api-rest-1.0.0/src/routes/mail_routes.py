from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import controllers.mail_controller as Controller

mailRoutes = Blueprint("mail", __name__, url_prefix="/mail")


@mailRoutes.route("/", methods=["POST"])
@cross_origin()
def EnviarEmail():
    parametros = request.json
    resp = Controller.EnviarEmail(
        parametros["email_emisor"],
        parametros["contrasena_emisor"],
        # parametros["servidor_smtp"],
        "smtp.gmail.com",
        # parametros["puerto_smtp"],
        "587",
        parametros["email_receptor"],
        parametros["nombre_completo"],
        parametros["grupo"],
        parametros["fecha_pronto"],
        parametros["monto_pronto"],
        parametros["referencia_pronto"],
        parametros["fecha_atraso"],
        parametros["monto_atraso"],
        parametros["referencia_atraso"],
    )
    print(f"ticket de pago enviado : {resp}")
    return jsonify(resp), 200
