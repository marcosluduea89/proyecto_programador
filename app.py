#!/usr/bin/env python
'''
API Registro de emprendimiento 
---------------------------
Autor: Ludueña Marcos
Version: 1.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
operaciones con clientes.

Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
NOTA: Si es la primera vez que se lanza este programa crear la base de datos
entrando a la siguiente URL
http://127.0.0.1:5000/reset

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

__author__ = "Marcos Ludueña"
__email__ = "marcosluduea89@gmail.com"
__version__ = "1.0"

import traceback
import io
import sys
import os
import base64
import json
import sqlite3
from datetime import datetime, timedelta

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect , url_for, session
import matplotlib
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

from clases import cliente 
from clases import operacion
from clases import producto
from clases import stock 
from clases import usuario

from config import config


# Crear el server Flask
app = Flask(__name__)

# Clave que utilizaremos para encriptar los datos
app.secret_key = "flask_session_key_inventada"

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db_config = config('db', config_path_name)
server_config = config('server', config_path_name)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_config['database']}"
# Asociamos nuestro controlador de la base de datos con la aplicacion
cliente.db.init_app(app)
operacion.db.init_app(app)
producto.db.init_app(app)
stock.db.init_app(app)
usuario.db.init_app(app)


# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/")
def index():
    try:
        
        if os.path.isfile(db_config['database']) == False:
            # Sino existe la base de datos la creo
            usuario.create_schema()
            operacion.create_schema()
            producto.create_schema()
            stock.create_schema()
            usuario.create_schema()

        # En el futuro se podria realizar una página de bienvenida
        return "<h1>prueba!!</h1>"
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/api")
def api():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido, aqui mostrare los endpoints!!</h1>"

        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/reset")
def reset():
    try:
        # Borrar y crear la base de datos
        if os.path.isfile(db_config['database']) == True:
        
            usuario.create_schema()
            operacion.create_schema()
            producto.create_schema()
            stock.create_schema()
            usuario.create_schema()

        result = "<h3>Base de datos re-generada!</h3>"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})



if __name__ == '__main__':
    print('Software fenix server start!')

    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)
