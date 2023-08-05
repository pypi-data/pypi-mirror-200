from email.message import EmailMessage
import ssl
import smtplib


def EnviarEmail(
    email_emisor,
    contrasena_emisor,
    servidor_smtp,
    puerto_smtp,
    email_receptor,
    nombre_completo,
    grupo,
    fecha_pronto,
    monto_pronto,
    referencia_pronto,
    fecha_atraso,
    monto_atraso,
    referencia_atraso,
):
    cuerpo = GenerarHTML(
        nombre_completo,
        grupo,
        email_receptor,
        fecha_pronto,
        monto_pronto,
        referencia_pronto,
        fecha_atraso,
        monto_atraso,
        referencia_atraso,
    )

    email = EmailMessage()
    email["From"] = email_emisor
    email["To"] = email_receptor
    email["Subject"] = "Referencia de pago cuatrimestral"

    # email.add_alternative("""<h1 style="color:red;">Test de html<h1>""", subtype="html")
    email.add_alternative(cuerpo, subtype="html")

    contexto = ssl.create_default_context()

    """ El servidor smtp y el puerto smtp depende del servidor de correo electronico que usemos """
    """ with smtplib.SMTP(servidor_smtp, puerto_smtp) as server:
        # print(email_emisor, contrasena_emisor)
        server.starttls(context=contexto)
        server.login(email_emisor, contrasena_emisor)
        server.sendmail(email_emisor, email_receptor, email.as_string()) """

    try:
        with smtplib.SMTP(servidor_smtp, puerto_smtp) as server:
            server.starttls(context=contexto)
            server.login(email_emisor, contrasena_emisor)
            server.sendmail(email_emisor, email_receptor, email.as_string())

            return "ok"
    except Exception as e:
        print("error al enviar ticket de pago: ", e)
        return "error"


def GenerarHTML(
    nombre_completo,
    grupo,
    correo_institucional,
    fecha_pronto,
    monto_pronto,
    referencia_pronto,
    fecha_atraso,
    monto_atraso,
    referencia_atraso,
):
    html = (
        """
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Recibo de pago cuatrimestral</title>
		<style>
			@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");

			a {
				text-decoration: none;
				color: dodgerblue;
			}

			* {
				padding: 0;
				margin: 0;
				box-sizing: border-box;
				font-family: "Roboto", sans-serif;
			}

			.container {
				display: grid;
				grid-template-columns: repeat(12, 1fr);
				grid-template-rows: repeat(4, auto);
				min-width: 700px;
				max-width: 900px;
				padding: 0 15px 0 15px;
				background-color: #f5f5f5;
				padding-bottom: 30px;
			}

			.cabecera {
				background-color: #fff;
				border: 1px solid rgba(128, 128, 128, 0.4);

				grid-column: 1 / 13;
				grid-row: 1/2;

				margin-top: 15px;

				border-radius: 50% 20% / 10% 40%;
				padding: 15px 20px 15px 20px;

				display: flex;
				justify-content: space-around;
			}

			.cabecera__contenedor-imagen {
				display: block;
				margin: auto;
				text-align: center;
				grid-column: 1/2;
			}

			.cabecera__contenedor-imagen--der {
				grid-column: 3/4;
			}

			.cabecera__contenedor-imagen__imagen {
				width: 140px;
				height: auto;
				padding: 0 10px 0 10px;
			}

			.cabecera__contenedor-texto {
				width: 70%;
				margin: auto;
				text-align: center;
			}

			.datos-alumnos {
				grid-column: 1 / 13;
				grid-row: 2/3;
				text-align: center;
				padding-top: 20px;
			}

			.bloque-datos {
				display: block;
				background-color: #fff;
				border: 1px solid rgba(128, 128, 128, 0.4);

				padding-top: 5px;
				padding-bottom: 15px;
				margin-top: 10px;

				border-radius: 25px;
			}

			.datos-bancarios {
				grid-column: 1 / 13;
				grid-row: 3/4;
				text-align: center;
				padding-top: 20px;
			}

			.pie-pagina {
				grid-column: 1 / 13;
				grid-row: 4/5;

				text-align: center;
				padding-top: 20px;
				padding-bottom: 20px;

				background-color: #fff;
				border: 1px solid rgba(128, 128, 128, 0.4);

				margin-top: 20px;

				border-radius: 5px 5px 5px 200px;
			}

			.linea-texto {
				margin-bottom: 5px;
				padding-left: 15px;
				display: flex;
			}

			.titulo1 {
				font-size: 15px;
				font-weight: 600;
				font-style: normal;
			}

			.titulo2 {
				font-size: 15px;
				font-weight: 500;
				font-style: normal;

				margin-left: 20px;
				margin-right: 10px;
			}

			.texto {
				font-size: 15px;
				font-weight: 400;
				font-style: normal;
			}

			button {
				align-self: center;
				font-family: Roboto, sans-serif;
				font-weight: 526;
				font-size: 17px;
				color: #fff;
				background-color: #0066cc;
				padding: 10px 30px;
				border: 2px solid #0066cc;
				box-shadow: rgba(0, 0, 0, 0.2) 0px 12px 28px 0px,
					rgba(0, 0, 0, 0.1) 0px 2px 4px 0px,
					rgba(255, 255, 255, 0.05) 0px 0px 0px 1px inset;
				border-radius: 50px;
				transition: 1000ms;
				transform: translateY(0);
				cursor: pointer;
				text-transform: uppercase;
				margin-top: 15px;
			}

			button:hover {
				transition: 1000ms;
				padding: 10px 50px;
				transform: translateY(-0px);
				background-color: #fff;
				color: #0066cc;
				border: solid 2px #0066cc;
			}

			.contenedor-boton {
				display: block;
			}
		</style>
	</head> 
    """
        + f"""
	<body>
		<div class="container">
			<div class="cabecera">
				<div class="cabecera__contenedor-imagen">
					<img
						src="https://enciclopediagro.mx/wp-content/uploads/egro/enciclopedia/tomo6/Foto-262.png"
						alt="univ-americana"
						class="cabecera__contenedor-imagen__imagen"
					/>
				</div>

				<div class="cabecera__contenedor-texto">
					<p class="titulo1">UNIVERSIDAD AMERICANA DE ACAPULCO</p>
					<p class="titulo1">AV. COSTERA MIGUEL ALEMAN N° 1756</p>
					<p class="titulo1">FRACC. MAGALLANES</p>
					<p class="titulo1">C.P 39670</p>
					<p class="titulo1">R.F.C. UAA-920320-TD5</p>
					<p class="titulo1">(744) 469 17 00</p>
				</div>

				<div class="cabecera__contenedor-imagen">
					<img
						src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Citibanamex_logo.svg/2560px-Citibanamex_logo.svg.png"
						alt="univ-americana"
						class="cabecera__contenedor-imagen__imagen"
					/>
				</div>
			</div>

			<div class="datos-alumnos">
				<p class="titulo1">FICHA DE PAGO</p>
				<div class="bloque-datos">
					<p class="titulo1">DATOS ALUMNO</p>
					<div class="linea-texto">
						<p class="titulo2">NOMBRE DEL ALUMNO:</p>
						<p class="texto">{nombre_completo}</p>
					</div>
					<div class="linea-texto">
						<p class="titulo2">GRUPO:</p>
						<p class="texto">{grupo}</p>
					</div>
					<div class="linea-texto">
						<p class="titulo2">CORREO INSTITUCIONAL:</p>
						<p class="texto">{correo_institucional}</p>
					</div>
				</div>
			</div>

			<div class="datos-bancarios">
				<p class="titulo1">
					DEPOSITAR EN CUALQUIER SUCURSAL
					<span style="text-decoration: underline">BANAMEX</span>
				</p>
				<div class="bloque-datos">
					<p class="titulo1">REFERENCIA DE PAGO</p>
					<div class="linea-texto">
						<p class="titulo2">PAGO HASTA EL:</p>
						<p class="texto">{fecha_pronto}</p>
					</div>
					<div class="linea-texto">
						<p class="titulo2">MONTO:</p>
						<p class="texto">${monto_pronto}</p>
					</div>
					<div class="linea-texto">
						<p class="titulo2">REFERENCIA:</p>
						<p class="texto">{referencia_pronto}</p>
					</div>
				</div>

				<div class="bloque-datos">
					<p class="titulo1">REFERENCIA DE PAGO CON RECARGO</p>
					<div class="linea-texto">
						<p class="titulo2">RECARGO A PARTIR DEL:</p>
						<p class="texto">{fecha_atraso}</p>
					</div>
					<div class="linea-texto">
						<p class="titulo2">MONTO:</p>
						<p class="texto">${monto_atraso}</p>
					</div>
					<div class="linea-texto">
						<p class="titulo2">REFERENCIA:</p>
						<p class="texto">{referencia_atraso}</p>
					</div>
				</div>
			</div>

			<div class="pie-pagina">
				<p class="texto">
					VIGENCIA HASTA EL ULTIMO DÍA DEL MES DE OCTUBRE
				</p>
				<p class="texto">RECARGOS POSTERIORES SEGÚN FECHA DE PAGO</p>
				<p class="texto">
					CUALQUIER DUDA NOS PUEDES CONSULTAR EN EL CORREO
					<a href="mailto:cobranzas@uaa.edu.mx" target="_blank"
						><b>COBRANZAS@UAA.EDU.MX</b></a
					>
				</p>
				<p class="texto">
					TAMBIEN YA PUEDES PAGAR EN LINEA CON LA PLATAFORMA BANAMEX,
					CLICK Y PAGA
				</p>

				<div class="contenedor-boton">
					<a
						style="text-decoration: none"
						href="https://clickypaga.com/univ-americana-cyp-b-639.html"
						><button>CLIK Y PAGA</button></a
					>
				</div>
			</div>
		</div>
	</body>
</html>




"""
    )
    return html
