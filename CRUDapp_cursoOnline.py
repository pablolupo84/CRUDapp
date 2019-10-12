from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import sqlite3

#-----------------FUNCIONES-----------------------

def infoAdicional():
	messagebox.showinfo("CRUDApp", "Gestion Base de Datos v2019")


def avisoLicencia():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU")


def conexionBBDD():
	miConexion = sqlite3.connect("Usuarios")
	miCursor = miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE DATOSUSUARIOS(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE_USUARIO VARCHAR(50),
			PASSWORD VARCHAR(50),
			APELLIDO VARCHAR(50),
			DIRECCION VARCHAR(50),
			COMENTARIOS VARCHAR(100))
		''')

		miConexion.commit()
		messagebox.showinfo("CRUDApp", "BBDD creada con exito!!")
		miConexion.close()
	except:
		messagebox.showwarning("CRUDApp - Atencion!", "BBDD YA EXISTE!!")

def salirAplicacion():
	opcion = messagebox.askquestion("Salir", "Desea salir de la aplicacion????", icon='warning')

	if opcion == "yes":
		raiz.destroy()


def leerInfoInputBox():
	listadata = [datacuadroNombre.get(), datacuadroPWD.get(),
			 datacuadroApellido.get(), datacuadroDireccion.get(), cuadroComentario.get(1.0, END)
			 ]
	return listadata


def limpiarCampos():

	dataCuadroID.set("")
	datacuadroNombre.set("")
	datacuadroPWD.set("")
	datacuadroApellido.set("")
	datacuadroDireccion.set("")
	cuadroComentario.delete(1.0,END)
	print("CRUDApp - Se borran todos los campos")

def Crear():
	
	try:
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		print("Successfully Connected to SQLite")

		listadata=leerInfoInputBox()
		print (listadata)
		count = miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES (NULL,?,?,?,?,?)", listadata)

		miConexion.commit()
		print("Record inserted successfully into DATOSUSUARIOS table ", miCursor.rowcount)
		messagebox.showinfo("CRUDApp", "BBDD creada con exito!!")
		miConexion.close()
	
	except:
		print("Failed to insert data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")

def Leer():
	
	try:
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID=" + dataCuadroID.get())
		listamiCursor=miCursor.fetchall() #recuperar los datos

		for usuario in listamiCursor:
			dataCuadroID.set(usuario[0])
			datacuadroNombre.set(usuario[1])
			datacuadroPWD.set(usuario[2])
			datacuadroApellido.set(usuario[3])
			datacuadroDireccion.set(usuario[4])
			cuadroComentario.delete(1.0, END)
			cuadroComentario.insert(1.0,usuario[5])
			
		miConexion.commit()
		print("Record read successfully")
		miConexion.close()
	except:
		print("Failed to Leer data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")


def Actualizar():
	
	try:	
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID=" + dataCuadroID.get())
		listamiCursor=miCursor.fetchall() #recuperar los datos
		
		for usuario in listamiCursor:
			
			data= leerInfoInputBox()
			data.append(dataCuadroID.get())

		sql_update_query = """UPDATE DATOSUSUARIOS set NOMBRE_USUARIO = ? ,PASSWORD = ?,APELLIDO = ?,DIRECCION = ?,COMENTARIOS = ? where ID = ?"""
		
		miCursor.execute(sql_update_query, data)

		miConexion.commit()
		messagebox.showinfo("CRUDApp", "BBDD aCTUALIZADA con exito!!")
		
		miCursor.close()
	except:
		print("Failed to Actualizar data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")



def Eliminar():

	try:
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		
		miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID=" + dataCuadroID.get())
		limpiarCampos()
		miConexion.commit()
		print("Record delete successfully")
		miConexion.close()
	except:
		print("Failed to Eliminar data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")


raiz = Tk()

raiz.title("CRUDApp - Gestion Base de Datos")
raiz.iconbitmap("Iconos/computer_1.ico")
# raiz.geometry("350x500")
# raiz.resizable(False,False)

barraMenu = Menu(raiz)
# raiz.config(menu=barraMenu,width=350,height=400)
raiz.config(menu=barraMenu,width=350,height=400)

BBDDmenu = Menu(barraMenu, tearoff=0)
BBDDmenu.add_command(label="Conectar", command=conexionBBDD)
BBDDmenu.add_command(label="Salir", command=salirAplicacion)
# BBDDmenu.add_separator()

Eliminarmenu = Menu(barraMenu, tearoff=0)
Eliminarmenu.add_command(label="Borrar Campos",command=limpiarCampos)

Crudmenu = Menu(barraMenu, tearoff=0)
Crudmenu.add_command(label="Create",command=lambda:Crear())
Crudmenu.add_command(label="Read",command=lambda:Leer())
Crudmenu.add_command(label="Update",command=lambda:Actualizar())
Crudmenu.add_command(label="Delete",command=lambda:Eliminar())

helpmenu = Menu(barraMenu, tearoff=0)
helpmenu.add_command(label="Licencia", command=avisoLicencia)
helpmenu.add_command(label="Acerca de...", command=infoAdicional)

barraMenu.add_cascade(label="BBDD", menu=BBDDmenu)
barraMenu.add_cascade(label="BORRAR", menu=Eliminarmenu)
barraMenu.add_cascade(label="CRUD", menu=Crudmenu)
barraMenu.add_cascade(label="AYUDA", menu=helpmenu)

#-----------------COMIENZO DE CAMPOS-----------------------

miFrame = Frame(raiz)
miFrame.pack()

dataCuadroID = StringVar()
datacuadroNombre = StringVar()
datacuadroPWD = StringVar()
datacuadroApellido = StringVar()
datacuadroDireccion = StringVar()


cuadroID = Entry(miFrame, textvariable=dataCuadroID)
cuadroID.grid(row=0, column=1, padx=10, pady=10)
cuadroID.config(fg="red", justify="center")

cuadroNombre = Entry(miFrame, textvariable=datacuadroNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)
cuadroNombre.config(justify="center")

cuadroPWD = Entry(miFrame, textvariable=datacuadroPWD)
cuadroPWD.grid(row=2, column=1, padx=10, pady=10)
cuadroPWD.config(justify="center", show="*")

cuadroApellido = Entry(miFrame, textvariable=datacuadroApellido)
cuadroApellido.grid(row=3, column=1, padx=10, pady=10)
cuadroApellido.config(justify="center")

cuadroDireccion = Entry(miFrame, textvariable=datacuadroDireccion)
cuadroDireccion.grid(row=4, column=1, padx=10, pady=10)
cuadroDireccion.config(justify="center")

cuadroComentario = Text(miFrame, width=16,heigh=5)
cuadroComentario.grid(row=5, column=1, padx=10, pady=10)
scrollVert=Scrollbar(miFrame,command=cuadroComentario.yview)
scrollVert.grid(row=5,column=2,sticky="nsew")

cuadroComentario.config(yscrollcommand=scrollVert.set)

#-----------------COMIENZO DE ETIQUETAS-----------------------

IDLabel = Label(miFrame, text="ID:")
IDLabel.grid(row=0, column=0, sticky="e",padx=10, pady=10)

NombreLabel = Label(miFrame, text="Nombre:")
NombreLabel.grid(row=1, column=0, sticky="e",padx=10, pady=10)

PWDLabel = Label(miFrame, text="Password:")
PWDLabel.grid(row=2, column=0,sticky="e", padx=10, pady=10)

ApellidoLabel = Label(miFrame, text="Apellido:")
ApellidoLabel.grid(row=3, column=0, sticky="e",padx=10, pady=10)

DireccionLabel = Label(miFrame, text="Direccion:")
DireccionLabel.grid(row=4, column=0, sticky="e",padx=10, pady=10)

ComentarioLabel = Label(miFrame, text="Comentarios:")
ComentarioLabel.grid(row=5, column=0,sticky="e", padx=10, pady=10)

#-----------------COMIENZO DE BOTONES-----------------------

miFrameInf = Frame(raiz)
miFrameInf.pack()

botonCreate = Button(miFrameInf, text="Create",command=lambda:Crear())
botonCreate.grid(row=1, column=0, sticky="e",padx=10, pady=10)

botonRead = Button(miFrameInf, text="Read",command=lambda:Leer())
botonRead.grid(row=1, column=1,sticky="e", padx=10, pady=10)

botonUpdate = Button(miFrameInf, text="Update",command=lambda:Actualizar())
botonUpdate.grid(row=1, column=2,sticky="e", padx=10, pady=10)

botonDelete = Button(miFrameInf, text="Delete",command=lambda:Eliminar())
botonDelete.grid(row=1, column=3,sticky="e", padx=10, pady=10)


raiz.mainloop()
