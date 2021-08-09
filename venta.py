#!/usr/bin/env python
'''
Software Fenix 1.1
---------------------------
Autor: Marcos Ludueña
Version: 1.1

'''

__author__ = "Marcos Ludueña "
__email__ = "marcosluduea89@gmail.com  "
__version__ = "1.1"


# En este archivo se encuentran todas las funcionalidades para la venta, por lo tanto importamos todas las clases 
# que la vinculan a ella

from os import name

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from models import db
from models import Cliente,Usuario,Operacion,Producto,Stock
import models


# Funcion para verificar el cliente segun su id (DNI)
def verificacion_cliente (dni):
    query = db.session.query(Cliente).filter(Cliente.dni==dni)
    validador = query.first()

    if validador is None:
        return []
        
    return validador

    pass
def agregar_cliente ():

    
    pass
def operacion_venta():

    # operacion.insert_operacion()
    # pass

    # def consulta_stock():
    #     pass
    # def venta():
    #     pass
    # def actualizar_stock():
        pass
def total():
    pass




