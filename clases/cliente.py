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

class Cliente(db.Model):
    __tablename__ = "cliente"
    dni = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    telefono = db.Column(db.Integer)
    direccion = db.Column(db.String)
    
    def __repr__(self):
        return f"Cliente {self.name} {self.apellido}, telefono{self.telefono} y direccion {self.direccion}"

def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(dni, nombre, apellido,telefono,direccion):
    # Crear un nuevo registro de clientes
    cliente = Cliente(dni= dni, nombre = nombre, apellido = apellido,telefono= telefono, direccion= direccion)

    # Agregar el registro de clientes a la DB
    db.session.add(cliente)
    db.session.commit()