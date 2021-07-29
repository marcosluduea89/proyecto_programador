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

class Stock(db.Model):
    __tablename__ = "stock"
    id_stock = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String)
    cantidad = db.Column(db.Integer)
    proveedor = db.Column(db.String)
    
    def __repr__(self):
        return f"{self.nombre_producto}, ingreso {self.cantidad}"

def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(nombre_producto, cantidad, proveedor):
    # Crear un nuevo registro de stock
    stock = Stock(nombre_producto=nombre_producto, cantidad= cantidad,proveedor=proveedor)

    # Agregar el registro de stock a la DB
    db.session.add(stock)
    db.session.commit()