import sys
import re
import mysql.connector
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtLocation, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidgetAction
from messagebox import msg_error, msg_about
#from database import DB


# ------------------------- CONEXION A LA BASE DE DATOS ------------------------ #
try:
    conexion = mysql.connector.connect(
        user = 'root', 
        password = 'root', 
        host = 'localhost', 
        database = 'portalesplaza',
        port = '3306'
        )
except:
    msg_error(title = 'Base de datos', message= 'Error, no se pudo conectar a la base de datos')


# ------------------------------ LOGIN ------------------------------ #
class VentanaLogin(QDialog):
    def __init__(self):
        super(VentanaLogin, self).__init__()
        loadUi("archivos/login.ui", self)        

        # --------- BOTONES ------- #
        #self.btn_registrar.clicked.connect(self.fun_registrar)
        self.btn_ingresar.clicked.connect(self.iniciar_sesion)

    # ----------- MANDA A LA VENTANA DE MENU PRINCIPAL ------------- #
    def gotoMenu(self):
        menu = VentanaMenu()
        ventana.addWidget(menu)
        ventana.setGeometry(310,115,1300,850) # x , y , w , h
        ventana.setCurrentIndex(ventana.currentIndex()+1)


    # ------------ Funcion de iniciar sesion -------------------- #
    def iniciar_sesion(self):
        usuario = self.line_usuario.text()
        contrasenia = self.line_contrasenia.text()

        if usuario == "":
            self.label_error.setText("Ingrese un usuario")
        elif contrasenia == "":
            self.label_error.setText("Ingrese una contraseña")
        elif not (len(usuario)>= 5 and len(usuario)<= 10 and re.search(r"^[A-Z]+[a-zA-Z0-9]*$", usuario)):
            msg_error(title= "Error Usuario", message= "El usuario debe: \n- Comenzar con una letra mayúscula \n- Tener entre 5 y 10 caracteres (letras o números) \n\n Intente de nuevo")
            self.line_usuario.clear()
            self.line_contrasenia.clear()
        elif not (len(contrasenia) == 8 and re.search(r"^[A-Z]+[a-zA-Z0-9]*$", contrasenia)):
            print(contrasenia)
            msg_error(title= "Error Contraseña", message= "La contraseña debe: \n- Comenzar con una letra mayúscula \n- Tener 8 caracteres (letras o números) \n\n Intente de nuevo")
            self.line_usuario.clear()
            self.line_contrasenia.clear()
        else:
            cursor = conexion.cursor()
            sql = f"SELECT user, password FROM login WHERE user = '{usuario}' and password = '{contrasenia}'"
            cursor.execute(sql)
            if cursor.fetchall():
                self.gotoMenu()
                # conexion.close()
            else:
                msg_error(title= 'Login', message= 'El usuario o la contraseña son incorrectos')
                self.line_usuario.clear()
                self.line_contrasenia.clear()
                self.label_error.clear()

    
    """
    #************ Registrar **********#
    def fun_registrar(self):
        self.mensajes_error()
        if self.validacion_usuario() == True and self.validacion_contrasenia() == True:
            showinfo("Registro", "El registro fué exitoso, ya puede iniciar sesión con este usuario")
            self.line_usuario.clear()
            self.line_contrasenia.clear()
            self.label_error.clear()
        else:
            print("Registro no exitoso")
    """

# ------------------------------ Menu ------------------------------ #
class VentanaMenu(QDialog):
    def __init__(self):
        super(VentanaMenu, self).__init__()
        loadUi("archivos/menu.ui", self)

        # ------- BOTONES ------- #
        self.btn_checkin.clicked.connect(self.gotoCheckIn)
        self.btn_checkout.clicked.connect(self.gotoCheckOut)
        self.btn_huespedes.clicked.connect(self.gotoHuespedes)
        self.btn_salir.clicked.connect(self.salir)

    # ----------- MANDA A LA VENTANA DE CHECK IN ------------- #
    def gotoCheckIn(self):
        checkin = VentanaCheckIn()
        ventana.addWidget(checkin)
        ventana.setFixedWidth(1300)
        ventana.setFixedHeight(850)
        ventana.setCurrentIndex(ventana.currentIndex()+1)
    
    # ----------- MANDA A LA VENTANA DE CHECK OUT ------------- #
    def gotoCheckOut(self):
        checkout = VentanaCheckOut()
        ventana.addWidget(checkout)
        ventana.setFixedWidth(1300)
        ventana.setFixedHeight(850)
        ventana.setCurrentIndex(ventana.currentIndex()+1)

    # ----------- MANDA A LA VENTANA DE EN CASA ------------- #
    def gotoHuespedes(self):
        huespedes = VentanaHuespedes()
        ventana.addWidget(huespedes)
        ventana.setFixedWidth(1300)
        ventana.setFixedHeight(850)
        ventana.setCurrentIndex(ventana.currentIndex()+1)

    # ----------- SALE DE LA APP ------------- #
    def salir(self):
        app.exit()

# ------------------------------ Check In ------------------------------ #
class VentanaCheckIn(QDialog):

    def __init__(self):
        super(VentanaCheckIn, self).__init__()
        loadUi("archivos/checkin.ui", self)

        # ------- BOTONES ------- #
        self.btn_buscar.clicked.connect(self.gotoBuscar)
        # ---- Registrar checkin ------- #
        self.btn_ingresar.clicked.connect(self.ingresar)
        # ------- Regresar ------- #
        self.login = VentanaLogin()
        self.btn_regresar.clicked.connect(self.login.gotoMenu)  
        # ---- Validaciones de cosas del designer ---- #
        self.line_telefono.setValidator(QtGui.QIntValidator())
        self.line_num_noches.setValidator(QtGui.QIntValidator())
        self.line_ingresar_pago.setValidator(QtGui.QIntValidator())
        self.comboBox_tipo_hab.currentIndexChanged.connect(self.actualizarComboBoxNumHab)

    def gotoBuscar(self):
        buscar = VentanaBuscar_CheckIn()
        ventana.addWidget(buscar)
        ventana.setFixedWidth(450)
        ventana.setFixedHeight(650)
        ventana.setCurrentIndex(ventana.currentIndex()+1)

    def actualizarComboBoxNumHab(self):
        def obtener_habitaciones(tipo_habitacion):
            cursor = conexion.cursor()
            sql = f"SELECT num_habitacion FROM habitaciones WHERE tipo_habitacion = '{tipo_habitacion}'"
            cursor.execute(sql)
            habitaciones = cursor.fetchall()   
            return [habitacion[0] for habitacion in habitaciones]

        tipo_habitacion = self.comboBox_tipo_hab.currentText()
        habitaciones = obtener_habitaciones(tipo_habitacion)

        self.comboBox_num_hab.clear()
        self.comboBox_num_hab.addItems(habitaciones)   
    
    def id_huesped(self):
        nombres = self.line_nombres.text()
        apellidos = self.line_apellidos.text()
        telefono = self.line_telefono.text()

        cursor = conexion.cursor()
        sql = f"SELECT id_huesped FROM huespedes WHERE nombres_huesped = '{nombres}' AND apellidos_huesped = '{apellidos}' AND telefono_huesped = '{telefono}'"
        cursor.execute(sql)
        id = cursor.fetchone()

    
    def id_habitación(self):
        numero_habitacion = self.comboBox_num_hab.itemText(self.comboBox_num_hab.currentIndex()) 

        cursor = conexion.cursor()
        sql = f"SELECT id_habitacion FROM habitaciones WHERE num_habitacion = '{numero_habitacion}'"
        cursor.execute(sql)
        id = cursor.fetchone()
        return id

    def ingresar(self):
        nombres = self.line_nombres.text()
        apellidos = self.line_apellidos.text()
        telefono = self.line_telefono.text()       
        tipo_hab = self.comboBox_num_hab.itemText(self.comboBox_tipo_hab.currentIndex()) 
        self.num_noches_texto = self.line_num_noches.text()
        self.pago_texto = self.line_ingresar_pago.text()

        if nombres == '' or apellidos == '' or telefono == '' or tipo_hab == '' or self.num_noches_texto == ''  or self.pago_texto == '':
            self.label_error.setText("No puede haber campos en blanco")
        elif not(re.search(r"[a-zA-Z ]+$", nombres)):
            self.label_error.setText("El nombre tiene que ser alfabético")
        elif not(re.search(r"[a-zA-Z ]+$", apellidos)):
            self.label_error.setText("El apellido tiene que ser alfabético")
        else:
            
            # ------------------ INGRESA DATOS A TABLA HUESPED ------------------- #
            cursor = conexion.cursor()
            sql = f"INSERT INTO huespedes (nombres_huesped, apellidos_huesped, telefono_huesped) VALUES ('{nombres}', '{apellidos}', '{telefono}')"
            cursor.execute(sql)
            conexion.commit()
            msg_about(title= 'Nuevo huésped', message= 'Huésped registrado con éxito')

            self.insertarEnChckin()
            
            self.label_error.clear()
            self.line_nombres.clear()
            self.line_apellidos.clear()
            self.line_telefono.clear()
            self.comboBox_tipo_hab.setCurrentIndex(0)
            self.comboBox_num_hab.setCurrentIndex(0)
            self.line_num_noches.clear()
            self.line_ingresar_pago.clear()


    def insertarEnChckin(self):
        nombres = self.line_nombres.text()
        apellidos = self.line_apellidos.text()
        telefono = self.line_telefono.text()

        numero_habitacion = self.comboBox_num_hab.itemText(self.comboBox_num_hab.currentIndex()) 

        num_noches = int(self.num_noches_texto)
        pago = int(self.pago_texto)

        # BUSCA EL ID DEL HUESPED
        cursor = conexion.cursor()
        sql = f"SELECT id_huesped FROM huespedes WHERE nombres_huesped = '{nombres}' AND apellidos_huesped = '{apellidos}' AND telefono_huesped = '{telefono}'"
        cursor.execute(sql)
        result_huesped = cursor.fetchone()

        #BUSCA EL ID DEL NUMERO DE LA HABITACION
        sql2 = f"SELECT id_habitacion FROM habitaciones WHERE num_habitacion = '{numero_habitacion}'"
        cursor.execute(sql2)
        result_habitacion = cursor.fetchone()

        if result_huesped and result_habitacion:
            id_huesped = result_huesped[0]
            id_habitacion = result_habitacion[0]

            sql3 = f"INSERT INTO checkin (fk_huesped, fk_habitacion, num_noches, pago) VALUES ('{id_huesped}', '{id_habitacion}','{num_noches}', '{pago}')"
            #sql = f"INSERT INTO checkin (num_noches, pago) VALUES ('{num_noches}', '{pago}')"
            cursor.execute(sql3)
            conexion.commit()
            msg_about(title= 'Check-In', message= 'Check-In realizado con éxito')

# ------------------------------ Buscar ------------------------------ #
class VentanaBuscar_CheckIn(QDialog):
    def __init__(self):
        super(VentanaBuscar_CheckIn, self).__init__()
        loadUi("archivos/buscar_checkin.ui", self)
        # ------- BOTONES ------- #
        self.menu = VentanaMenu()
        self.btn_cancelar.clicked.connect(self.menu.gotoCheckIn)
        self.btn_nuevo.clicked.connect(self.gotoNuevoHuesped)
        self.line_buscar.textEdited.connect(self.buscar)
        
        # ----------------- Tabla ---------------- #
        self.table_buscar.setColumnWidth(0,350)       
        self.cargarTablaBuscar() 

    def cargarTablaBuscar(self):
        cursor = conexion.cursor()
        sql = "SELECT nombre_completo FROM huespedes"
        cursor.execute(sql)
        tabla_huespedes = cursor.fetchall()
        self.table_buscar.setRowCount(len(tabla_huespedes))

        # Agregar los datos al QTableWidget
        for row in range(len(tabla_huespedes)):
            item = QtWidgets.QTableWidgetItem(tabla_huespedes[row][0])
            self.table_buscar.setItem(row, 0, item)

    def buscar(self):
        nombre_completo = self.line_buscar.text()
        cursor = conexion.cursor()
        sql = f"SELECT nombre_completo FROM huespedes WHERE nombre_completo = '{nombre_completo}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.table_buscar.setColumnCount(1)
        self.table_buscar.setRowCount(len(result))

        # Agregar los resultados al QTableWidget
        for row in range(len(result)):
            item = QtWidgets.QTableWidgetItem(result[row][0])
            self.table_buscar.setItem(row, 0, item)

    def gotoNuevoHuesped(self):
        nuevoHuesped = VentanaNuevoHuesped()
        ventana.addWidget(nuevoHuesped)
        ventana.setFixedWidth(430)
        ventana.setFixedHeight(460)
        ventana.setCurrentIndex(ventana.currentIndex()+1)

# ------------------------------ Nuevo huesped------------------------------ #
class VentanaNuevoHuesped(QDialog):
    def __init__(self):
        super(VentanaNuevoHuesped, self).__init__()
        loadUi("archivos/nuevo_huesped.ui", self)

        # ------- BOTONES ------- #
        self.checkin = VentanaCheckIn()
        self.btn_cancelar.clicked.connect(self.checkin.gotoBuscar)
        self.btn_aceptar.clicked.connect(self.nuevoHuesped)
        self.line_telefono.setValidator(QtGui.QIntValidator())

    def nuevoHuesped(self):
        nombres = self.line_nombres.text()
        apellidos = self.line_apellidos.text()
        telefono = self.line_telefono.text()
        if len(nombres)==0 or len(apellidos)==0 or len(telefono)==0:
            self.label_error.setText("No puede haber campos en blanco")
        elif not(re.search(r"[a-zA-Z ]+$", nombres)):
            self.label_error.setText("El nombre tiene que ser alfabético")
        elif not(re.search(r"[a-zA-Z ]+$", apellidos)):
            self.label_error.setText("El apellido tiene que ser alfabético")
        else:
            cursor = conexion.cursor()
            sql = f"INSERT INTO huespedes (nombres_huesped, apellidos_huesped, telefono_huesped) VALUES ('{nombres}', '{apellidos}', '{telefono}')"
            cursor.execute(sql)
            conexion.commit()
            msg_about(title= 'Nuevo huésped', message= 'Huésped registrado con éxito')
            self.label_error.clear()
            self.line_nombres.clear()
            self.line_apellidos.clear()
            self.line_telefono.clear()

# ------------------------------ Check Out ------------------------------ #
class VentanaCheckOut(QDialog):
    def __init__(self):
        super(VentanaCheckOut, self).__init__()
        loadUi("archivos/checkout.ui", self)

        # ------- BOTONES ------- #
        self.login = VentanaLogin()
        self.btn_regresar.clicked.connect(self.login.gotoMenu)

        self.table_checkout.setColumnWidth(0,100) 
        self.table_checkout.setColumnWidth(1,400) 
        self.table_checkout.setColumnWidth(2,130) 
        self.table_checkout.setColumnWidth(3,225) 
        self.table_checkout.setColumnWidth(4,225)

        self.line_habitacion.setValidator(QtGui.QIntValidator())
        self.line_habitacion.textEdited.connect(self.buscar_por_habitacion)


    def buscar_por_habitacion(self):
        num_habitacion = self.line_habitacion.text()

        cursor = conexion.cursor()
        sql = f"SELECT c.id_checkin, h.nombre_completo, r.num_habitacion, c.num_noches, c.pago FROM checkin c INNER JOIN habitaciones r ON c.fk_habitacion = r.id_habitacion INNER JOIN huespedes h ON c.fk_huesped = h.id_huesped WHERE r.num_habitacion = '{num_habitacion}'"
        cursor.execute(sql)
        datos_checkin = cursor.fetchall()
        self.table_checkout.setColumnCount(5)
        self.table_checkout.setRowCount(len(datos_checkin))

        # Llenar la tabla con los resultados
        for fila, datos in enumerate(datos_checkin):
            for columna, valor in enumerate(datos):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.table_checkout.setItem(fila, columna, item)  



# ------------------------------ En Casa ------------------------------ #
class VentanaHuespedes(QDialog):
    def __init__(self):
        super(VentanaHuespedes, self).__init__()
        loadUi("archivos/huespedes.ui", self)

        # ------- BOTONES ------- #
        self.login = VentanaLogin()
        self.btn_regresar.clicked.connect(self.login.gotoMenu)

#main
app = QApplication(sys.argv)
login = VentanaLogin()
ventana = QtWidgets.QStackedWidget()
ventana.addWidget(login)
ventana.setGeometry(735,420,450,240)
ventana.show()
try: 
    sys.exit(app.exec_())
except: 
    print("Saliendo")
    conexion.close()