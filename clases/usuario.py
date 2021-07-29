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


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuario"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    
    def __repr__(self):
        return f"Usuario con id: {self.id_usuario},  {self.nombre},{self.apellido}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(nombre, apellido):
    # Crear un nuevo registro de usuario
    usuario = Usuario(nombre= nombre, apellido= apellido)

    # Agregar el registro de usuario a la DB
    db.session.add(usuario)
    db.session.commit()