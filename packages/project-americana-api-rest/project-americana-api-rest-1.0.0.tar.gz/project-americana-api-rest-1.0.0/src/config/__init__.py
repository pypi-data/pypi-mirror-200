# coding utf-8
""" Modulo para las configuraciones de Flask y de la base de datos de Firebird 1.5

Available functions:
    - DevelopmentConfig: Configuración de desarrollo
    - ProductionConfig: Configuración de producción

Available const:
    - cursor: Cursor de la conexión a la base de datos
"""

# IMPORTACIONES
import os
import firebirdsql
import dotenv

dotenv.load_dotenv()

# CONFIGURACIÓN
class Config:
    """Base config"""

    # SECRET_KEY=""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    DEVELOPMENT = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    DEVELOPMENT = False
    FLASK_ENV = "production"


# DATABASE
if os.getenv("ENV") == "DEVELOPMENT":
    connection = firebirdsql.connect(
        host=os.getenv("DEVELOPMENT_HOST"),
        database=os.getenv("DEVELOPMENT_DATABASE"),
        user=os.getenv("DEVELOPMENT_USER"),
        password=os.getenv("DEVELOPMENT_PASSWORD"),
    )
    print("LOADED DEVELOPMENT DATABASE CONFIGURATION")
else:
    # SIGNIFICA QUE ESTAMOS EN UN ENTORNO DE PRODUCCIÓN
    print("PRODUCTION ENVIRONMENT")
    connection = firebirdsql.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

cursor = connection.cursor()
