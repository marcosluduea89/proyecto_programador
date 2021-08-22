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
from sqlalchemy.sql import expression
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

from models import db
from models import *
import models 
from venta import verificacion_cliente
from venta import buscador_cliente

from models import actualizar_stock, insert_cliente, insert_productos,insert_stock,insert_usuario


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
        # renderizamos la pagina principal
        return render_template('home.html')
 
                
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/reset")
def reset():
    try:
        # Borrar y crear la base de datos e insertar productos

        
        models.create_schema()
        models.insert_productos()
        models.insert_usuario(nombre='Marcos',apellido='ludueña')
        models.insert_stock()
            
        
        return ("<h3>Base de datos re-generada!</h3>")
            

    except:
        
        return jsonify({'trace': traceback.format_exc()})
        


@app.route("/venta", methods= ['GET','POST'] )
# verificar si el cliente se encuentra en la base de datos segun su DNI
# formulario html con un input
def venta():
    if request.method == 'GET':
        # Si entré por "GET" es porque acabo de cargar la página
        try:
            session['cliente'] =''
            return render_template('autentificacion.html')
            
        except:
            return jsonify({'trace': traceback.format_exc()})
    
    if request.method == 'POST':
        try:
            dni = str(request.form.get('dni'))
            # # llamamos a la funcion busqueda cuyo parametro será dni
            check = verificacion_cliente(int(dni))

            if check is True:
                nombre_cliente = buscador_cliente(int(dni))
                session['cliente'] = nombre_cliente
                

                return redirect(url_for('operacion')) 
            else:
                return render_template('autentificacion2.html')
            
          
        except:
            return jsonify({'trace': traceback.format_exc()})


@app.route("/operacion",methods=['GET', 'POST','PUT'])
def operacion():
    if request.method == 'GET':
        try:
            
            if 'cliente' in session:
                nombre_cliente = session['cliente']

                
                total_stock_canasto_ropa = models.consultar_stock(nombre='canasto_ropa')
                total_stock_canasto_matero= models.consultar_stock(nombre='canasto_matero')
                total_stock_bandejas_exhibidoras= models.consultar_stock(nombre='bandejas_exhibidoras')
                total_stock_bandejas_pintadas = models.consultar_stock(nombre='bandejas_pintadas')
                total_stock_anillos = models.consultar_stock(nombre='anillos')
                total_stock_paneritas_mimbre = models.consultar_stock(nombre='paneritas_mimbre')
                total_stock_paneritas_madera = models.consultar_stock(nombre='paneritas_madera')
            
                return render_template ('operacion.html',nombre_cliente=nombre_cliente,
                total_stock_canasto_ropa= total_stock_canasto_ropa, total_stock_canasto_matero=total_stock_canasto_matero,
                total_stock_bandejas_exhibidoras=total_stock_bandejas_exhibidoras,total_stock_bandejas_pintadas=total_stock_bandejas_pintadas,
                total_stock_anillos=total_stock_anillos,total_stock_paneritas_mimbre=total_stock_paneritas_mimbre,
                total_stock_paneritas_madera=total_stock_paneritas_madera)
            


        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        # en este caso debemos crear multiples operaciones, ya que cada producto es independiente
        
        cantidad_canasto_ropa= str(request.form.get('canasto_ropa'))
        try:
            int(cantidad_canasto_ropa) 
            nombre = 'canasto_ropa'
            cantidad = cantidad_canasto_ropa
            try:
                #chequeamos que el total solicitado no sea mayor al que hay disponible en stock
                total_stock = models.consultar_stock(nombre)
                if  total_stock > int(cantidad) :

                    models.actualizar_stock (nombre,cantidad)
                #     #falta realizar html de usuario, por el momento pondremos '1' marcos
                    id_usuario = 1 # esto prodria solicitarlo como un post tambien   
                #     #falta realizar la logica por ahora pondremos un numero x
                    precio_final =models.consultar_preciofinal(nombre,cantidad)
                    
                    models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            except:
                return ("< no hay stock o no los suficientes del producto seleccionado</h3>" )
                
        except:
            pass
            
         
        cantidad_canasto_matero = str(request.form.get('canasto_matero'))
        try:
            int(cantidad_canasto_matero) 
            nombre = 'canasto_matero'
            cantidad = cantidad_canasto_matero
            try:
                total_stock = models.consultar_stock(nombre)
                if  total_stock > int(cantidad) :
                    models.actualizar_stock (nombre,cantidad)
                    id_usuario = 1
                    precio_final = models.consultar_preciofinal(nombre,cantidad)
                    models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            except:
                pass
        except:
            pass        

        cantidad_bandejas_exhibidoras = str(request.form.get('bandejas_exhibidoras'))
        try:
            int(cantidad_bandejas_exhibidoras)
            nombre = 'bandejas_exhibidoras'
            cantidad = cantidad_bandejas_exhibidoras
            try:
                total_stock = models.consultar_stock(nombre)
                if  total_stock > int(cantidad) :
                    models.actualizar_stock (nombre,cantidad)
                    id_usuario = 1
                    precio_final = models.consultar_preciofinal(nombre,cantidad)
                    models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            except:
                pass
        except:
            pass            

        cantidad_bandejas_pintadas = str(request.form.get('bandejas_pintadas'))
        try:
            int(cantidad_bandejas_pintadas) 
            nombre = 'bandejas_pintadas'
            cantidad = cantidad_bandejas_pintadas
            try:
                total_stock = models.consultar_stock(nombre)
                if  total_stock > int(cantidad) :
                    models.actualizar_stock (nombre,cantidad)    
                    id_usuario = 1
                    precio_final = models.consultar_preciofinal(nombre,cantidad)
                    models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            except:
                pass
        except:
            pass            

        cantidad_anillos =  str(request.form.get('anillos'))
        try:
            int(cantidad_anillos) 
            nombre = 'anillos'
            cantidad = cantidad_anillos
            try:
                total_stock = models.consultar_stock(nombre)
                if  total_stock > int(cantidad) :
                    models.actualizar_stock (nombre,cantidad)
                    id_usuario = 1
                    precio_final = models.consultar_preciofinal(nombre,cantidad)
                    models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            except:
                pass
        except:
            pass            

        cantidad_paneritas_mimbre =  str(request.form.get('paneritas_mimbre'))
        try:
            int(cantidad_paneritas_mimbre) 
            nombre = 'paneritas_mimbre'
            cantidad = cantidad_paneritas_mimbre
            try: 
                total_stock = models.consultar_stock(nombre)
                if  total_stock > int(cantidad) :
                    models.actualizar_stock (nombre,cantidad)
                    id_usuario = 1
                    precio_final = models.consultar_preciofinal(nombre,cantidad)
                    models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            except:
                pass
        except:
            pass

        cantidad_paneritas_madera= str(request.form.get('paneritas_madera'))
        try: 
            int(cantidad_paneritas_madera) 
            nombre = 'paneritas_madera'
            cantidad = cantidad_paneritas_madera
            try:
                total_stock = models.consultar_stock(nombre)                
                if  total_stock > int(cantidad) :
                    models.actualizar_stock (nombre,cantidad)
                    id_usuario = 1
                    precio_final = models.consultar_preciofinal(nombre,cantidad)
                    models.insert_operacion (str(nombre),int(cantidad),int(id_usuario),int(precio_final))
            except:
                pass
        except:
            pass

            

        # return redirect(url_for('operacion'))
        return  render_template('operacion2.html')

                
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
        return redirect(url_for('venta'))


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

@app.route("/operaciones")
def operaciones():
    try:

        limit_str = str(request.args.get('limit'))
        offset_str = str(request.args.get('offset'))

        limit = 0
        offset = 0

        if(limit_str is not None) and (limit_str.isdigit()):
            limit = int(limit_str)

        if(offset_str is not None) and (offset_str.isdigit()):
            offset = int(offset_str)

        # Obtener el reporte
        data = models.report(limit=limit, offset=offset)

        return render_template('tabla_ultimas_operaciones.html', data=data)
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/infocliente")
def infocliente():
    try:

        if 'cliente' in session:
            nombre_cliente = session['cliente']

        cliente_id = models.buscar_id_cliente(nombre_cliente)



        # Obtener el reporte
        data = models.report_cliente(int(cliente_id))

        return render_template('tabla_info_cliente.html', data=data)
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/clientes")
def clientes():
    try:

        limit_str = str(request.args.get('limit'))
        offset_str = str(request.args.get('offset'))

        limit = 0
        offset = 0

        if(limit_str is not None) and (limit_str.isdigit()):
            limit = int(limit_str)

        if(offset_str is not None) and (offset_str.isdigit()):
            offset = int(offset_str)

        # Obtener el reporte
        data = models.report_clientes(limit=limit, offset=offset)

        return render_template('tabla_clientes.html', data=data)
    except:
        return jsonify({'trace': traceback.format_exc()})    

@app.route ("/stock", methods= ['GET', 'PUT']  )
def stock ():
    if request.method == 'GET':

        try:
            limit_str = str(request.args.get('limit'))
            offset_str = str(request.args.get('offset'))

            limit = 0
            offset = 0

            if(limit_str is not None) and (limit_str.isdigit()):
                limit = int(limit_str)

            if(offset_str is not None) and (offset_str.isdigit()):
                offset = int(offset_str)

        # Obtener el reporte
            data = models.reporte_stock(limit=limit, offset=offset)
            
         
            return render_template('tabla_stock.html', data=data)

            

        except:
            return jsonify({'trace': traceback.format_exc()})

  
    if request.method == 'POST':

        # cantidad_canasto_ropa = (request.form.get ('cantidad_canasto_ropa'))


        pass




if __name__ == '__main__':
    print('*************************************')
    print('')
    print('Software fenix server start!')
    print('')
    print('*************************************')

    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)



