## Indice de contenido
- [1. Introducción al proyecto](#1-introducción-al-proyecto)
- [2. Configuración de desarrollo](#2-configuración-de-desarrollo)
	- [2.1 Instalación de Python y Pip](#21-instalación-de-python-y-pip)
		- [2.1.1 Creación de entorno virtual e instalación de dependencias](#211-creación-de-entorno-virtual-e-instalación-de-dependencias)
	- [2.2 Configuración de variables de entorno](#22-configuración-de-variables-de-entorno)
- [3. Revision de rutas](#3-revision-de-rutas)
	- [3.1 Root](#31-root)
	- [3.2 Datafields](#32-datafields)
	- [3.3 Movil](#33-movil)
	- [3.4 Recibos](#34-recibos)
- [4. Notas](#4-notas)
- [5. TODO](#5-todo)
- [Links de utilidad](#links-de-utilidad)
	- [Base de datos](#base-de-datos)
	- [Flask](#flask)
	- [Firebird](#firebird)
	- [Commits](#commits)

# 1. Introducción al proyecto
Esta es la primera parte de tres de un proyecto general para la consulta y automatización de generación de correos electrónicos para la escuela americana. 

Siendo la segunda parte una aplicación de de interfaz de usuario hecha en electron mediante la cual se hará la creación y envío automático de correos electrónicos y siendo la tercera parte el desarrollo de una aplicación móvil.

Este modulo se centra en la obtención de datos de una base de datos en Firebird v1.5. Funcionando como una API REST para el consumo de los dos módulos adicionales.

# 2. Configuración de desarrollo
Esta api funciona con la version 1.5 de firebird. Para instalarlo puede visitar la [documentación oficial 🔗](https://firebirdsql.org/en/firebird-1-5/) 

Una vez clonado el repositorio mediante : 
` git clone https://github.com/Cuervos-Blancos/project-americana_api-rest `

## 2.1 Instalación de Python y Pip
Tenemos que comprobar si tenemos el entorno correcto, el proyecto funciona con [python 3.9🔗](https://www.python.org/downloads/).

Si deseamos saber que version de python tenemos instalada, podemos hacerlo mediante el comando: 
` python --version `

De igual manera es util tener una version actualizada de `pip`. En este proyecto se una pip 22.
Se puede comprobar la version de pip instalada mediante el comando: 
` pip --version `

Una vez que se ha clonado el repositorio y se ha revisado que se tiene una version reciente de python. Es de utilidad  revisar la integridad de la base de datos, es bastante probable que la base de datos se encuentre corrupta o dañada (Debido a la version de firebird), para ello vaya a la sección [utilidad🔗](#links-de-utilidad) y revise el enlace que se refiere a la integridad de la base de datos.

### 2.1.1 Creación de entorno virtual e instalación de dependencias
Para evitar el conflicto entre distintos proyectos de python y distintas versiones en los módulos, es menester la creación de un entorno virtual.

Para ello, abrirá una consola de comandos en la carpeta raíz del proyecto.
Desde ahora se asumirá que se esta en un entorno ***Windows***, no obstante, si se en otro entorno, siempre puede [buscar la equivalencia de comandos🔗](https://www.google.com).

El primer paso es instalar el modulo que permite crear entornos virtuales, esto mediante el comando:

`pip install virtualenv`

Se puede comprobar si se instalo correctamente utilizando el comando:

`virtualenv --version`

En el cmd, ubicado en la carpeta raiz del proyecto usara el comando: 

`virtualenv venv`

Esto creara un entorno virtual en la carpeta `venv` (Puede personalizar el nombre de la carpeta modificando el comando).

Creando el siguiente árbol de carpetas:
```
root
 |
 |- env
 |- src
 |   |- config
 |   |- controllers
 |   |- models
 |   |- routes
 |   |- utils
 |   |- app.py
 |   |- __main__.py
 |- requirements.txt
```

Si creó correctamente el entorno virtual, lo activaremos mediante el siguiente comando:

` ./venv/Scripts/activate `

Y deberá notar que ahora su linea de comandos tiene el prefijo `(venv)`

Ahora, instale las dependencias, para ello usaremos el comando:

` pip install -r requirements.txt `

Y se deberán instalar todos los módulos correctamente.


## 2.2 Configuración de variables de entorno
Para este proyecto necesitamos instanciar cinco variables de entorno(En para el modo de desarrollo) :
- ENV=DEVELOPMENT
- DEVELOPMENT_HOST
- DEVELOPMENT_DATABASE
- DEVELOPMENT_USER
- DEVELOPMENT_PASSWORD

Si se va a desplegar, debemos instanciar:
- ENV=PRODUCTION
- HOST
- DATABASE
- USER
- PASSWORD

Existen dos forma de hacerlo, desde *powershell* y desde *cmd*.

Ejemplificando desde powershell:

*Establecer*
```powershell
$env:ENTORNO='development'
```

*Ver*
```powershell
$env:ENTORNO
```

En este caso tenemos instalado el modulo [python-dotenv 0.21.0🔗](https://pypi.org/project/python-dotenv/). Asi que tendremos que crear un archivo `.env` a la altura de las carpetas `src` y `venv`. Lo cual nos dejara el siguiente árbol de directorios:
```
root
 |- venv
 |- src
 |- .env
```
En el archivo `.env` necesitamos instanciar las variables mencionadas anteriormente, para ello, podemos usar el siguiente formato, pero personalizado con sus datos(*Es importante que se mantengan los mismo nombres y las mayúsculas*):
``` dotenv
ENV=DEVELOPMENT
DEVELOPMENT_HOST=localhost
DEVELOPMENT_DATABASE=C:\Users\project\DATOS.GDB
DEVELOPMENT_USER=admin
DEVELOPMENT_PASSWORD=admin
```

# 3. Revision de rutas
Actualmente la API cuenta con cuatro rutas. Para verificar que estén funcionando primero iniciaremos la aplicación mediante el comando:

` python .\src\__main__.py`

*Asumiendo que se encuentre en `root`*

Y deberá recibir un mensaje de [*Flask*🔗](https://flask-es.readthedocs.io/installation/) verificando que la aplicación de inicio de manera correcta.

Para revisar las rutas, puede hacerlo desde el navegador o mediante un cliente como [insomnia🔗](https://insomnia.rest/) el cual es que se utilizo en la realización de este proyecto.

## 3.1 Root
La ruta raíz devolverá algo de información de la api, puede consultar esta ruta al inicio para verificar que todo esta funcionando correctamente.
Esto mediante:

*GET* `http://localhost:5000/`

Esta ruta devuelve:
```json
{
	"authors": [
		"🍃 Carlos C.",
		"Abarca Lopez"
	],
	"description": "Modulo de RestApi del proyecto de automatización de envío de correos electrónicos para la Americana",
	"name": "rest_api_python3-firebird",
	"version": "0.1"
}
```


## 3.2 Datafields
Esta ruta esta pensada para rellenar los datafields de la interfaz de usuario con los datos actualizados de los ciclos escolares, periodos, mes, carreras y grupos.

*GET* `http://localhost:5000/datafields`

Devuelve:

```json
{
	"codigo_corto": [
		{
			"codigo_corto": "2022-2022 C3",
			"periodo": 27
		},
		{
			"codigo_corto": "2022/2023",
			"periodo": 16
		},
		{
			"codigo_corto": "2022-2022 C2",
			"periodo": 29
		},
		{
			"codigo_corto": "2022/2023-1",
			"periodo": 30
		},
		{
			"codigo_corto": "2022/2023-2",
			"periodo": 31
		}
	],
	"codigogrupo": [
		"FIC 3010",
		"2010 FIC",
		"2010 LCRP",
		"2010 FD",
		"0510 FD",
		"4010 LCRP",
		"8510 LCRP",
		"6510 LCRP",
		"4010 FD",
		"6510 FD",
		"8510 FD"
	],
	"mes": [
		1,
		2,
		3,
		4,
		5,
		6,
		7,
		8,
		9,
		10,
		11,
		12
	],
	"nivel": [
		"FD",
		"MAEST",
		"FCONT",
		"FDSUA",
		"FI",
		"FP",
		"FADMN",
		"FAET",
		"FCRP",
		"FGAS",
		"FA",
		"FCEA",
		"FCS",
		"PREPA",
		"CLE",
		"DGA",
		"LA",
		"LD",
		"EPCH"
	]
}

```

## 3.3 Movil
Esta ruta esta pensada para rellenar los datos de la aplicación Movil.
Debemos pasar el numero del alumno como parámetro en la petición.

*GET* `http://localhost:5000/mobile/:numero_alumno`

Esto devuelve:

```json
[
	{
		"materno": "LOPEZ ",
		"nivel": "FA",
		"nombre": "MARCELA ESTEFANIA",
		"numeroalumno": 10143,
		"pagado": "S",
		"paterno": "GUINTO "
	}
]
```

## 3.4 Recibos
Esta ruta devuelve los datos necesarios para generar recibos de cobro
*Esta implementada, pero no existe retorno de datos, vea* [TODO](#5-todo)

Recibe los parámetros de nivel, codigogrupo, periodo y mes. Regresa los datos que coincidan con **todos** los parámetros:

*GET* `http://localhost:5000/recibos/:nivel/:codigogrupo/:periodo/:mes`

# 4. Notas
Si desea hacer un commit, tome en cuenta que usamos la metodología de [conventional commits🔗](https://www.conventionalcommits.org/en/v1.0.0/)

# 5. TODO
- [ ] Agregar Unit Test para las rutas
- [ ] Agregar validación de datos para los parámetros de la request
- [ ] Agregar a README.md que tablas y columnas selecciona cada ruta (documentar mejor)
- [ ] Verificar como obtener el concepto de pago
- [ ] Obtener parámetros validos para obtener resultados en la ruta /recibos


# Links de utilidad
## Base de datos
Errores de consistencia en la base de datos o base de datos corrupta [🔗](https://ib-aid.com/en/articles/internal-gds-software-consistency-check/)

*Por seguridad no podemos poner el link a la base de datos*

## Flask
Documentación de Flask [🔗](https://flask-es.readthedocs.io/installation/)

Que hace el modo DEBUG en Flask [🔗](https://www.educba.com/flask-debug-mode/)


## Firebird
Documentación del Driver *pyfirebirdsql* [🔗](https://pyfirebirdsql.readthedocs.io/en/latest/tutorial.html)

Documentación de Firebird [🔗](https://firebirdsql.org/en/firebird-rdbms/)

Link de Firebird 1.5 [🔗](https://firebirdsql.org/en/firebird-1-5/)

## Commits
Documentación conventional commits [🔗](https://www.conventionalcommits.org/en/v1.0.0/)

Video explicativo en YT [🔗](https://youtu.be/Cp_SHttVTi0)

FreeCodeCamp ConventionalCommits [🔗](https://www.freecodecamp.org/espanol/news/como-escribir-un-buen-mensaje-de-commit/)