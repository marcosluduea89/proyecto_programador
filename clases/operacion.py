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

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker, relationship
from sqlalchemy import func

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Operacion(db.Model):
    __tablename__ = "operacion"
    id_operacion = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String)
    id_producto = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    id_usuario = db.Column(db.Integer)
    precio_final = db.Column(db.Integer)
    
    def __repr__(self):
        return f"""Operación {self.id_operacion} en el dia {self.fecha},
         cuyo producto es {self.id_producto} fue atendido por {self.usuario} y precio final es {self.precio} """

def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(fecha,id_producto, cantidad, id_usuario,precio_final):
    # Crear un nuevo registro de operacion
    operacion = Operacion(fecha,id_producto, cantidad, id_usuario,precio_final)

    # Agregar el registro de operacion a la DB
    db.session.add(operacion)
    db.session.commit()