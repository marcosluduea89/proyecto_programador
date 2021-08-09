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

from datetime import datetime
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
        return f"Cliente {self.nombre} {self.apellido}, telefono{self.telefono} y direccion {self.direccion}"

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    
    def __repr__(self):
        return f"Usuario con id: {self.id},  {self.nombre},{self.apellido}"

class Operacion(db.Model):
    __tablename__ = "operacion"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    id_producto = db.Column(db.Integer, ForeignKey("producto.id"))
    cantidad = db.Column(db.Integer)
    id_usuario = db.Column(db.Integer, ForeignKey("usuario.id"))
    precio_final = db.Column(db.Integer)
    
    producto = relationship("Producto")
    usuario = relationship("Usuario")

    def __repr__(self):
        return f"""Operación {self.id} en el dia {self.fecha},
         cuyo producto es {self.id_producto} fue atendido por {self.usuario} y precio final es {self.precio_final} """

class Producto(db.Model):
    __tablename__ = "producto"
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String)
    dimension = db.Column(db.String)
    precio = db.Column(db.Integer)
    
 
    
    def __repr__(self):
        return f" Producto nuevo: {self.nombre_producto}, id_producto: {self.id}"

class Stock(db.Model):
    __tablename__ = "stock"
    id= db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.String, ForeignKey("producto.id"))
    cantidad = db.Column(db.Integer)
    proveedor = db.Column(db.String)
    
    producto = relationship("Producto")
    
    def __repr__(self):
        return f"{self.id_producto}, ingreso {self.cantidad}"

def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()

def insert_cliente(dni, nombre, apellido,telefono,direccion):
    # Crear un nuevo registro de clientes
    cliente = Cliente(dni= dni, nombre = nombre, apellido = apellido,telefono= telefono, direccion= direccion)

    # Agregar el registro de clientes a la DB
    db.session.add(cliente)
    db.session.commit()

def insert_usuario(nombre, apellido):
    # Crear un nuevo registro de usuario
    usuario = Usuario(nombre= nombre, apellido= apellido)

    # Agregar el registro de usuario a la DB
    db.session.add(usuario)
    db.session.commit()

def insert_operacion(nombre, cantidad,id_usuario,precio_final):
    # Crear un nuevo registro de operacion

    fecha = datetime.now()
    numeroid = buscar_id_producto(nombre)
    id_producto = numeroid

    nueva_operacion = Operacion(fecha=fecha, cantidad=cantidad,precio_final=precio_final)
    nueva_operacion.id_producto= id_producto
    nueva_operacion.id_usuario=id_usuario

    # Agregar el registro de operacion a la DB
    db.session.add(nueva_operacion)
    db.session.commit()

def insert_productos():
    def insertar (nombre_producto,dimension,precio):
    # Crear un nuevo producto
        producto_nuevo = Producto(nombre_producto=nombre_producto,dimension=dimension,precio=precio)

        # Agregar el producto a la DB
        db.session.add(producto_nuevo)
        db.session.commit()

    productos = [('canasto_ropa' ,'20x30',100),('canasto_matero' ,'25x30',150),
                ('bandejas_exhibidoras' ,'25x30',150),('bandejas_pintadas' ,'25x35',200),
                ('anillos' ,'25',40),('paneritas_mimbre' ,'25x35',250),('paneritas_madera','25x35',300)]
    
    for row in productos:
        nombre_producto,dimension,precio = row
        insertar (nombre_producto,dimension,int(precio))
        
def insert_stock(nombre_producto, cantidad, proveedor):
    # Crear un nuevo registro de stock
    stock = Stock(nombre_producto=nombre_producto, cantidad= cantidad,proveedor=proveedor)

    # Agregar el registro de stock a la DB
    db.session.add(stock)
    db.session.commit()

def buscar_id_producto(nombre):
    query = db.session.query(Producto).filter(Producto.nombre_producto == nombre)
    producto = query.first()
    numeroid= producto.id

    return numeroid

def busqueda():
    query = db.session.query(Cliente)
    todos = query.all()
    dni = [x.dni for x in todos]
    telefono = [x.telefono for x in todos]
    

    return dni,telefono

