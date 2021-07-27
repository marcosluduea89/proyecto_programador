#!/usr/bin/env python
'''
Software Fenix 1.1
---------------------------
Autor: Marcos Ludueña
Version: 1.1

'''

__author__ = "Marcos Ludueña "
__email__ = "marcosluduea89@gmail.com  "
__version__ = "1.0"


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = "Producto"
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String)
    dimension = db.Column(db.String)
    precio = db.Column(db.Integer)
    
 
    
    def __repr__(self):
        return f" Producto nuevo: {self.nombre_producto}, id_producto: {self.id_producto}"

def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(nombre_producto, dimension, precio):
    # Crear un nuevo producto
    producto = Producto(nombre_producto= nombre_producto, dimension=dimension, precio=precio)

    # Agregar el producto a la DB
    db.session.add(producto)
    db.session.commit()