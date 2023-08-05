from email.message import EmailMessage
import ssl
import smtplib


def LogIn(email_emisor, contrasenia):
    email = EmailMessage()
    email["From"] = email_emisor
    email["To"] = email_emisor
    email["Subject"] = "Correo de verificacion sistema tickets de pago"

    email.set_content(
        "Correo para verificar que puede enviar correos automatizados desde esta dirección"
    )

    contexto = ssl.create_default_context()

    try:
        with smtplib.SMTP("smtp.gmail.com", "587") as server:
            server.starttls(context=contexto)
            server.login(email_emisor, contrasenia)
            server.sendmail(email_emisor, email_emisor, email.as_string())

            return "ok"
    except Exception as e:
        print("error al enviar ticket de pago: ", e)
        return "error"
