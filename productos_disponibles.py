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


# En este archivo se crearan los objetos o proctos disponibles, dicho de otra manera
# se añadirá y completara automaticamente la tabla producto 
# # 
# class Producto(db.Model):
#     __tablename__ = "producto"
#     id = db.Column(db.Integer, primary_key=True)
#     nombre_producto = db.Column(db.String)
#     dimension = db.Column(db.String)
#     precio = db.Column(db.Integer)
# Los productos son:
            # canasto_ropa ,20x30,100
            # canasto_matero,25x30,150
            # bandejas_exhibidoras,25x30,150
            # bandejas_pintadas,25x35,200
            # anillos ,25,40
            # paneritas_mimbre,25x35,250
            # paneritas_madera,25x35,300
            
def insertar_productos ():
    productos = [('canasto_ropa' ,'20x30',100),('canasto_matero' ,'25x30',150),
                ('bandejas_exhibidoras' ,'25x30',150),('bandejas_pintadas' ,'25x35',200)
                ('anillos' ,'25',40),('paneritas_mimbre' ,'25x35',250),'paneritas_madera','25x35',300]
    pass