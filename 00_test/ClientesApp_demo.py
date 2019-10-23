from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import sqlite3

#-----------------FUNCIONES-----------------------

def infoAdicional():
	messagebox.showinfo("ClientesApp_demo", "Gestion Base de Datos Pablo Lupo v2019")


def avisoLicencia():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU - Pablo Lupo")


def salirAplicacion():
	opcion = messagebox.askquestion(
		"Salir", "Desea salir de la aplicacion????", icon='warning')

	if opcion == "yes":
		raiz.destroy()

def crearDB():
	crearDB_Clientes()
	crearDB_ventas()

def crearDB_Clientes():
	miConexion = sqlite3.connect("CLIENTES")
	miCursor = miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE CLIENTES(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE_USUARIO VARCHAR(50),
			TELEFONO VARCHAR(50),
			COMENTARIOS VARCHAR(100))
		''')

		miConexion.commit()
		messagebox.showinfo("ClientesApp_demo", "BBDD CLIENTES creada con exito!!")
		miConexion.close()
	except:
		messagebox.showinfo("ClientesApp_demo", "BBDD CLIENTES YA EXISTE!!")

def crearDB_ventas():
	miConexion = sqlite3.connect("VENTAS")
	miCursor = miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE VENTAS(
			ID_VENTAS INTEGER PRIMARY KEY AUTOINCREMENT,
			ID_USUARIO INTEGER,
			DESCRIPCION VARCHAR(50),
			TOTAL_VENTA REAL,
			DESCUENTO REAL)  
		''')

		miConexion.commit()
		messagebox.showinfo("ClientesApp_demo", "BBDD Ventas creada con exito!!")
		miConexion.close()
	except:
		messagebox.showinfo("ClientesApp_demo", "BBDD Ventas YA EXISTE!!")


def leerInfoInputBox():
	listadata = [datacuadroNombre.get(),datacuadroTelefono.get(), cuadroComentario.get('1.0', 'end')
			 ]
	return listadata


def borrarInputBox():

	dataCuadroID.set("")
	datacuadroNombre.set("")
	datacuadroTelefono.set("")
	cuadroComentario.delete('1.0', 'end')
	print("ClientesApp_demo - Se borran todos los campos")

def InsertarData():
	
	try:
		miConexion = sqlite3.connect("CLIENTES")
		miCursor = miConexion.cursor()
		print("Successfully Connected to SQLite")

		listadata=leerInfoInputBox()
		print (listadata)
		count = miCursor.execute("INSERT INTO CLIENTES VALUES (NULL,?,?,?)", listadata)

		miConexion.commit()
		print("Record inserted successfully into CLIENTES table ", miCursor.rowcount)
		messagebox.showinfo("ClientesApp_demo", "BBDD creada con exito!!")
		miConexion.close()
	
	except:
		print("Failed to insert data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")

def ReadData():
	
	try:
		miConexion = sqlite3.connect("CLIENTES")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM CLIENTES")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):
				dataCuadroID.set(datos[0])
				datacuadroNombre.set(datos[1])
				datacuadroTelefono.set(datos[2])
				cuadroComentario.delete('1.0', 'end')
				cuadroComentario.insert('1.0',datos[3])
				continue
		miConexion.commit()
		print("Record read successfully")
		miConexion.close()
	except:
		print("Failed to ReadData data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")


def updateData():
	
	try:	
		miConexion = sqlite3.connect("CLIENTES")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM CLIENTES")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):			
				data= leerInfoInputBox()
				data.append(IDleido)

		sql_update_query = """UPDATE CLIENTES set NOMBRE_USUARIO = ? ,TELEFONO = ?,COMENTARIOS = ? where ID = ?"""
		
		miCursor.execute(sql_update_query, data)

		#print (sql_update_query)
		miConexion.commit()
		print("Record Updated successfully")
		miCursor.close()
	except:
		print("Failed to updateData data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")



def deleteData():

	try:
		miConexion = sqlite3.connect("CLIENTES")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM CLIENTES")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):
				miCursor.execute("DELETE FROM CLIENTES WHERE ID=" + IDleido)
		borrarInputBox()
		miConexion.commit()
		print("Record delete successfully")
		miConexion.close()
	except:
		print("Failed to deleteData data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")


raiz = Tk()

raiz.title("ClientesApp_demo - Gestion Base de Datos")
raiz.iconbitmap("Iconos/computer_1.ico")
# raiz.geometry("350x500")
# raiz.resizable(False,False)

barraMenu = Menu(raiz)
# raiz.config(menu=barraMenu,width=350,height=400)
raiz.config(menu=barraMenu)

BBDDmenu = Menu(barraMenu, tearoff=0)
BBDDmenu.add_command(label="Conectar", command=crearDB)
BBDDmenu.add_command(label="Salir", command=salirAplicacion)
# BBDDmenu.add_separator()

borrarmenu = Menu(barraMenu, tearoff=0)
borrarmenu.add_command(label="Borrar Campos",command=borrarInputBox)

Crudmenu = Menu(barraMenu, tearoff=0)
Crudmenu.add_command(label="Nuevo Cliente",command=lambda:InsertarData())
Crudmenu.add_command(label="Buscar por ID",command=lambda:ReadData())
Crudmenu.add_command(label="Actualizar",command=lambda:updateData())
Crudmenu.add_command(label="Borrar por ID",command=lambda:deleteData())

helpmenu = Menu(barraMenu, tearoff=0)
helpmenu.add_command(label="Licencia", command=avisoLicencia)
helpmenu.add_command(label="Acerca de...", command=infoAdicional)

barraMenu.add_cascade(label="BBDD", menu=BBDDmenu)
barraMenu.add_cascade(label="BORRAR", menu=borrarmenu)
barraMenu.add_cascade(label="CLIENTES", menu=Crudmenu)
barraMenu.add_cascade(label="AYUDA", menu=helpmenu)

#-----------------COMIENZO DE CAMPOS-----------------------

miFrame = Frame(raiz, width=350, height=400)
miFrame.pack()

dataCuadroID = StringVar()
datacuadroNombre = StringVar()
datacuadroTelefono = StringVar()


cuadroID = Entry(miFrame, textvariable=dataCuadroID)
cuadroID.grid(row=0, column=1, padx=10, pady=10,columnspan=3)
cuadroID.config(fg="red", justify="center")

cuadroNombre = Entry(miFrame, textvariable=datacuadroNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=1,columnspan=3)
cuadroNombre.config(justify="center")

cuadroTelefono = Entry(miFrame, textvariable=datacuadroTelefono)
cuadroTelefono.grid(row=2, column=1, padx=10, pady=10,columnspan=3)
cuadroTelefono.config(justify="center")

cuadroComentario = Text(miFrame, width=20,heigh=10)
cuadroComentario.grid(row=3, column=1, padx=10, pady=10,columnspan=3)
scrollVert=Scrollbar(miFrame,command=cuadroComentario.yview)
scrollVert.grid(row=3,column=4,sticky="nsew")

cuadroComentario.config(yscrollcommand=scrollVert.set)

#-----------------COMIENZO DE ETIQUETAS-----------------------

IDLabel = Label(miFrame, text="ID: ")
IDLabel.grid(row=0, column=0, padx=10, pady=10)

NombreLabel = Label(miFrame, text="Nombre: ")
NombreLabel.grid(row=1, column=0, padx=10, pady=10)

TelefonoLabel = Label(miFrame, text="Telefono: ")
TelefonoLabel.grid(row=2, column=0, padx=10, pady=10)

ComentarioLabel = Label(miFrame, text="Comentarios: ")
ComentarioLabel.grid(row=3, column=0, padx=10, pady=10)

#-----------------COMIENZO DE BOTONES-----------------------

#botonCreate = Button(miFrame, text="Create", width=8,command=lambda:InsertarData())
#botonCreate.grid(row=4, column=0, padx=10, pady=10)

#botonRead = Button(miFrame, text="Read", width=8,command=lambda:ReadData())
#botonRead.grid(row=4, column=1, padx=10, pady=10)

#botonUpdate = Button(miFrame, text="Update", width=8,command=lambda:updateData())
#botonUpdate.grid(row=4, column=2, padx=10, pady=10)

#botonDelete = Button(miFrame, text="Delete", width=8,command=lambda:deleteData())
#botonDelete.grid(row=4, column=3, padx=10, pady=10)


raiz.mainloop()

