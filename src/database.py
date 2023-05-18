import mysql.connector
from tkinter import messagebox
#from main import *

class DB():
    def __init__(self):
        # ------------------------- CONEXION A LA BASE DE DATOS ------------------------ #
        try:
            self.conexion = mysql.connector.connect(
                user = 'root', 
                password = 'root', 
                host = 'localhost', 
                database = 'portalesplaza',
                port = '3306'
                )
        except:
            messagebox.showerror(title = 'Base de datos', message= 'Error, no se pudo conectar a la base de datos')
        print("Database conectada correctamente", self.conexion)

    def iniciar_sesion(self,usuario,contrasenia):
        #login = VentanaLogin()
        cursor = self.conexion.cursor()
        sql = "SELECT user, password FROM login WHERE user = '"+usuario+"' and password = '"+contrasenia+"'"
        cursor.execute(sql)
        cursor.fetchall()
    
    def cargarTablaBuscar(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM huespedes"
        cursor.execute(sql)
        tabla_huespedes = cursor.fetchall()
        return tabla_huespedes 