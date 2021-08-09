#!/usr/bin/env python
'''
API Registro de ventas
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



from re import template
import traceback
import io
import sys
import os
import base64
import json
import sqlite3
from datetime import datetime, timedelta
from flask_sqlalchemy import model
from flask_sqlalchemy.model import Model

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect , url_for, session
import matplotlib
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

from models import busqueda, db, insert_cliente
from models import Cliente,Usuario,Operacion,Producto,Stock
import models
from venta import verificacion_cliente


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


models.db.init_app(app)

# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/")
def index():
    try:
        
        if os.path.isfile(db_config['database']) == False:
            # Sino existe la base de datos la creo
            
            models.create_schema()

        # En el futuro se podria realizar una página de bienvenida
        return """<h1>#Lo primero que debe hacer es loguearse,luego establecer el stock de los productos.
                      #Si queremos realizar una venta y no hay stock, se informa de tal evento.
                      # Solo hay dos opciones de ingreso, Venta y Consulta </h1>"""
                
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/api")
def api():
    try:
        # Imprimir los distintos endopoints disponibles
        #inicio y creacion de base de datos
        result = "<h2>[GET] /reset --> borrar y crear la base de datos</h2>"
        #logueo y logout
        result += "<h2>[GET] /login --> HTML con el formulario de ingreso de usuario</h2>"
        result += "<h2>[POST] /login --> ingresar el nombre de usuario por JSON</h2>"
        result += "<h2>[GET] /usuario --> Pagina de bienvenida del usuario</h2>"
        result += "<h2>[GET] /logout --> Terminar la sesion</h2>"
        #endpoints de funcionalidades de la app
        result += "<h2>elegir operacion/</h2>"
        result += "<h2>elegir operacion/1 _Venta:</h2>"
        result += "<h2>elegir operacion/2 _Consulta:</h2>"

        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})




@app.route("/reset")
def reset():
    try:
        # Borrar y crear la base de datos e insertar productos
        if os.path.isfile(db_config['database']) == True:
        
            models.create_schema()
            models.insert_productos()
            models.insert_usuario(nombre='Marcos',apellido='ludueña')
            

        result = "<h3>Base de datos re-generada!</h3>"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/venta", methods= ['GET','POST'] )
# verificar si el cliente se encuentra en la base de datos segun su DNI
# formulario html con un input
def venta():
    if request.method == 'GET':
        # Si entré por "GET" es porque acabo de cargar la página
        try:
            return render_template('login.html')
            
        except:
            return jsonify({'trace': traceback.format_exc()})
    
    if request.method == 'POST':
        try:
            dni = str(request.form.get('dni'))
            # llamamos a la funcion busqueda cuyo parametro será dni
            check = verificacion_cliente(dni) 

            if dni == check:
                return redirect(url_for('operacion'))
        except:
            return jsonify({'trace': traceback.format_exc()})


@app.route("/comparativa")
def comparativa(): 
    dni,telefono = models.busqueda()

    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(dni,telefono)
    ax.set_ylabel("Edad")
    ax.set_xlabel("ID")

        
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)  # Cerramos la imagen para que no consuma memoria del sistema
    return Response(output.getvalue(), mimetype='image/png')      
        
@app.route("/operacion",methods=['GET', 'POST'])
def operacion():
    if request.method == 'GET':
        try:
            
            return render_template ('operacion.html')


        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        # en este caso debemos crear multiples operaciones, ya que cada producto es independiente
        cantidad_canasto_ropa= str(request.form.get('canasto_ropa'))
        
        if int(cantidad_canasto_ropa) > 0 :
            nombre = 'canasto_ropa'
            cantidad = cantidad_canasto_ropa
            #     #falta realizar tabla de usuario, por el momento pondremos '1' marcos
            id_usuario = 1 # esto prodria solicitarlo como un post tambien   
            #     #falta realizar la logica por ahora pondremos un numero x
            precio_final = 300
            models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            
         
        cantidad_canasto_matero = str(request.form.get('canasto_matero'))
        if int(cantidad_canasto_matero) > 0:
            nombre = 'canasto_matero'
            cantidad = cantidad_canasto_matero
            id_usuario = 1
            precio_final = 300
            models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))

        cantidad_bandejas_exhibidoras = str(request.form.get('bandejas_exhibidoras'))
        if int(cantidad_bandejas_exhibidoras) > 0:
            nombre = 'bandejas_exhibidoras'
            cantidad = cantidad_bandejas_exhibidoras
            id_usuario = 1
            precio_final = 300
            models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            

        cantidad_bandejas_pintadas = str(request.form.get('bandejas_pintadas'))
        if int(cantidad_bandejas_pintadas) > 0 :
            nombre = 'bandejas_pintadas'
            cantidad = cantidad_bandejas_pintadas
            id_usuario = 1
            precio_final = 300
            models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            

        cantidad_anillos =  str(request.form.get('anillos'))
        if int(cantidad_anillos) > 0 :
            nombre = 'anillos'
            cantidad = cantidad_anillos
            id_usuario = 1
            precio_final = 300
            models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            

        cantidad_paneritas_mimbre =  str(request.form.get('paneritas_mimbre'))
        if int(cantidad_paneritas_mimbre) > 0 :
            nombre = 'paneritas_mimbre'
            cantidad = cantidad_paneritas_mimbre
            id_usuario = 1
            precio_final = 300
            models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))


        cantidad_paneritas_madera= str(request.form.get('paneritas_madera'))
        if int(cantidad_paneritas_madera) > 0:
            nombre = 'paneritas_madera'
            cantidad = cantidad_paneritas_madera
            id_usuario = 1
            precio_final = 300
            models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))


            

        # return redirect(url_for('operacion'))
        return  "<h3>Post realizado!</h3>"

                
@app.route("/registrocliente",methods=['GET', 'POST'])
def registrocliente ():
    if request.method == 'GET':
        try:
            return render_template ('registrocliente.html')

        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        dni = str(request.form.get('dni'))
        nombre = str(request.form.get('nombre'))
        apellido= str(request.form.get('apellido'))
        telefono = str(request.form.get('telefono'))
        direccion = str(request.form.get('direccion'))


        models.insert_cliente(int(dni),nombre,apellido,int(telefono),direccion)
        return redirect(url_for('operacion'))


@app.route("/registrousuario",methods=['GET', 'POST'])
def registrousuario ():
    if request.method == 'GET':
        try:
            return render_template ('registrousuario.html')

        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        
        nombre = str(request.form.get('nombre'))
        apellido= str(request.form.get('apellido'))
        

        models.insert_cliente(nombre,apellido)
        return redirect(url_for('operacion'))



if __name__ == '__main__':
    print('*************************************')
    print('')
    print('Software fenix server start!')
    print('')
    print('*************************************')

    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)



