from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import sqlite3


def infoAdicional():
	messagebox.showinfo("CRUDApp", "Gestion Base de Datos v2019")


def avisoLicencia():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU")


def salirAplicacion():
	opcion = messagebox.askquestion(
		"Salir", "Desea salir de la aplicacion????", icon='warning')

	if opcion == "yes":
		raiz.destroy()


def crearDB():
	miConexion = sqlite3.connect("Usuarios")
	miCursor = miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE USUARIOS(
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
		messagebox.showinfo("CRUDApp", "BBDD YA EXISTE!!")


def leerInfoInputBox():
	listadata = [datacuadroNombre.get(), datacuadroPWD.get(),
			 datacuadroApellido.get(), datacuadroDireccion.get(), cuadroComentario.get('1.0', 'end')
			 ]
	return listadata


def borrarInputBox():

	dataCuadroID.set("")
	datacuadroNombre.set("")
	datacuadroPWD.set("")
	datacuadroApellido.set("")
	datacuadroDireccion.set("")
	cuadroComentario.delete('1.0', 'end')
	print("CRUDApp - Se borran todos los campos")

def InsertarData():
	
	try:
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		print("Successfully Connected to SQLite")

		listadata=leerInfoInputBox()
		print (listadata)
		count = miCursor.execute("INSERT INTO Usuarios VALUES (NULL,?,?,?,?,?)", listadata)

		miConexion.commit()
		print("Record inserted successfully into Usuarios table ", miCursor.rowcount)
		messagebox.showinfo("CRUDApp", "BBDD creada con exito!!")
		miConexion.close()
	
	except:
		print("Failed to insert data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")

def ReadData():
	
	try:
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM Usuarios")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):
				dataCuadroID.set(datos[0])
				datacuadroNombre.set(datos[1])
				datacuadroPWD.set(datos[2])
				datacuadroApellido.set(datos[3])
				datacuadroDireccion.set(datos[4])
				cuadroComentario.delete('1.0', 'end')
				cuadroComentario.insert('1.0',datos[5])
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
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM Usuarios")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):			
				data= leerInfoInputBox()
				data.append(IDleido)

		sql_update_query = """UPDATE Usuarios set NOMBRE_USUARIO = ? ,PASSWORD = ?,APELLIDO = ?,DIRECCION = ?,COMENTARIOS = ? where ID = ?"""
		
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
		miConexion = sqlite3.connect("Usuarios")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM Usuarios")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):
				miCursor.execute("DELETE FROM Usuarios WHERE ID=" + IDleido)
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

raiz.title("CRUDApp - Gestion Base de Datos")
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
Crudmenu.add_command(label="Create",command=lambda:InsertarData())
Crudmenu.add_command(label="Read",command=lambda:ReadData())
Crudmenu.add_command(label="Update",command=lambda:updateData())
Crudmenu.add_command(label="Delete",command=lambda:deleteData())

helpmenu = Menu(barraMenu, tearoff=0)
helpmenu.add_command(label="Licencia", command=avisoLicencia)
helpmenu.add_command(label="Acerca de...", command=infoAdicional)

barraMenu.add_cascade(label="BBDD", menu=BBDDmenu)
barraMenu.add_cascade(label="BORRAR", menu=borrarmenu)
barraMenu.add_cascade(label="CRUD", menu=Crudmenu)
barraMenu.add_cascade(label="AYUDA", menu=helpmenu)

miFrame = Frame(raiz, width=350, height=400)
miFrame.pack()

dataCuadroID = StringVar()
datacuadroNombre = StringVar()
datacuadroPWD = StringVar()
datacuadroApellido = StringVar()
datacuadroDireccion = StringVar()


cuadroID = Entry(miFrame, textvariable=dataCuadroID)
cuadroID.grid(row=0, column=1, padx=10, pady=10,columnspan=2)
cuadroID.config(fg="red", justify="center")

cuadroNombre = Entry(miFrame, textvariable=datacuadroNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10,columnspan=2)
cuadroNombre.config(justify="center")

cuadroPWD = Entry(miFrame, textvariable=datacuadroPWD)
cuadroPWD.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
cuadroPWD.config(justify="center", show="*")

cuadroApellido = Entry(miFrame, textvariable=datacuadroApellido)
cuadroApellido.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
cuadroApellido.config(justify="center")

cuadroDireccion = Entry(miFrame, textvariable=datacuadroDireccion)
cuadroDireccion.grid(row=4, column=1, padx=10, pady=10, columnspan=2)
cuadroDireccion.config(justify="center")

cuadroComentario = Text(miFrame, width=20,heigh=10)
cuadroComentario.grid(row=5, column=1, padx=10, pady=10, columnspan=2)

IDLabel = Label(miFrame, text="ID: ")
IDLabel.grid(row=0, column=0, padx=10, pady=10)

NombreLabel = Label(miFrame, text="Nombre: ")
NombreLabel.grid(row=1, column=0, padx=10, pady=10)

PWDLabel = Label(miFrame, text="Password: ")
PWDLabel.grid(row=2, column=0, padx=10, pady=10)

ApellidoLabel = Label(miFrame, text="Apellido: ")
ApellidoLabel.grid(row=3, column=0, padx=10, pady=10)

DireccionLabel = Label(miFrame, text="Direccion: ")
DireccionLabel.grid(row=4, column=0, padx=10, pady=10)

ComentarioLabel = Label(miFrame, text="Comentarios: ")
ComentarioLabel.grid(row=5, column=0, padx=10, pady=10)

botonCreate = Button(miFrame, text="Create", width=8,command=lambda:InsertarData())
botonCreate.grid(row=6, column=0, padx=10, pady=10)

botonRead = Button(miFrame, text="Read", width=8,command=lambda:ReadData())
botonRead.grid(row=6, column=1, padx=10, pady=10)

botonUpdate = Button(miFrame, text="Update", width=8,command=lambda:updateData())
botonUpdate.grid(row=6, column=2, padx=10, pady=10)

botonDelete = Button(miFrame, text="Delete", width=8,command=lambda:deleteData())
botonDelete.grid(row=6, column=3, padx=10, pady=10)


raiz.mainloop()
