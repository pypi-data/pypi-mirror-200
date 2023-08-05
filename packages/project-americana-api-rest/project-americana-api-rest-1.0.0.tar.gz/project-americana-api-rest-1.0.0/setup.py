from setuptools import setup, find_packages

setup(
    name='project-americana-api-rest',
    version='1.0.0',
    description='API REST para Project Americana',
    url='https://github.com/TU_USUARIO/project-americana-api-rest',
    author='Tu Nombre',
    author_email='tu_correo@ejemplo.com',
    packages=find_packages(),
    install_requires=[
        'Flask==2.0.1',
        'flask-restful==0.3.9'
    ],
)

