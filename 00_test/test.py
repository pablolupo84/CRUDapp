#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import sqlite3

class ClientesFrame(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        #-----------------COMIENZO DE CAMPOS-----------------------
        self.miFrame = Frame(self, width=350, height=400)
        self.miFrame.pack()

        #self.dataCuadroID = StringVar()
        self.datacuadroNombre = StringVar()
        self.datacuadroTelefono = StringVar()

        #self.cuadroID = Entry(self.miFrame, textvariable=self.dataCuadroID)
        #self.cuadroID.grid(row=0, column=1, padx=10, pady=10,columnspan=3)
        #self.cuadroID.config(fg="red", justify="center")

        self.cuadroNombre = Entry(self.miFrame, textvariable=self.datacuadroNombre)
        self.cuadroNombre.grid(row=1, column=1, padx=10, pady=1,columnspan=3)
        self.cuadroNombre.config(justify="center")

        self.cuadroTelefono = Entry(self.miFrame, textvariable=self.datacuadroTelefono)
        self.cuadroTelefono.grid(row=2, column=1, padx=10, pady=10,columnspan=3)
        self.cuadroTelefono.config(justify="center")

        #self.cuadroComentario = Text(self.miFrame, width=20,heigh=10)
        #self.cuadroComentario.grid(row=3, column=1, padx=10, pady=10,columnspan=3)
        #self.scrollVert=Scrollbar(self.miFrame,command=self.cuadroComentario.yview)
        #self.scrollVert.grid(row=3,column=4,sticky="nsew")

        #self.cuadroComentario.config(yscrollcommand=self.scrollVert.set)

        #-----------------COMIENZO DE ETIQUETAS-----------------------

        #self.IDLabel = Label(self.miFrame, text="ID: ")
        #self.IDLabel.grid(row=0, column=0, padx=10, pady=10)

        self.NombreLabel = Label(self.miFrame, text="Nombre: ")
        self.NombreLabel.grid(row=1, column=0, padx=10, pady=10)

        self.TelefonoLabel = Label(self.miFrame, text="Telefono: ")
        self.TelefonoLabel.grid(row=2, column=0, padx=10, pady=10)

        #self.ComentarioLabel = Label(self.miFrame, text="Comentarios: ")
        #self.ComentarioLabel.grid(row=3, column=0, padx=10, pady=10)

        #-----------------Visor de Clientes-----------------------

        self.miFrame_3 = Frame(self)
        self.miFrame_3.pack()

        self.tituloLabel=Label(self.miFrame_3,text="Clientes",fg="blue",bg="white",font=("Times New Roman",20))
        self.tituloLabel.grid(row=0, column=1, padx=10, pady=10,sticky="we")

        self.treeVentas = ttk.Treeview(self.miFrame_3,columns = ("ID_USUARIO","NOMBRE_USUARIO","TELEFONO","COMENTARIO"))   
        self.treeVentas.grid(row=1,column=1,padx=10,pady=10)
        self.treeVentas['show']='headings'
        self.treeVentas.heading('#0', text='column0', anchor=tk.W)
        self.treeVentas.heading('#1', text='ID_USUARIO', anchor=tk.W)
        self.treeVentas.heading('#2', text='NOMBRE_USUARIO', anchor=tk.W)
        self.treeVentas.heading('#3', text='TELEFONO', anchor=tk.W)
        self.treeVentas.heading('#4', text='COMENTARIO', anchor=tk.W)
        

        self.treeVentas.column('#0',width=70,minwidth=70,stretch=tk.YES)
        self.treeVentas.column('#1',width=70,minwidth=70,stretch=tk.YES)
        self.treeVentas.column('#2',width=120,minwidth=120,stretch=tk.YES)
        self.treeVentas.column('#3',width=90,minwidth=90,stretch=tk.YES)
        self.treeVentas.column('#4',width=120,minwidth=120,stretch=tk.YES)

   
        for row in self.consultarClientes():
            self.treeVentas.insert('',END, values=row)

        self.scrollVert2=Scrollbar(self.miFrame_3,command=self.treeVentas.yview)
        self.scrollVert2.grid(row=1,column=2,sticky="nsnew")
        self.treeVentas.config(yscrollcommand=self.scrollVert2.set)


        #-----------------COMIENZO DE BOTONES-----------------------
        self.miFrame_2 = Frame(self)
        self.miFrame_2.pack()

        self.botonCreateDB = Button(self.miFrame_2, text="Create DB", width=10,command=lambda:self.crearDB())
        self.botonCreateDB.grid(row=5, column=2, padx=10, pady=10)
        
        self.botonCreate = Button(self.miFrame_2, text="Nuevo", width=10,command=lambda:self.InsertarData())
        self.botonCreate.grid(row=4, column=0, padx=10, pady=10)

        self.botonReadID =Button(self.miFrame_2, text="Buscar ID", width=10,command=lambda:self.ReadDataID())
        self.botonReadID.grid(row=4, column=1, padx=10, pady=10)

        self.botonReadUSER =Button(self.miFrame_2, text="Buscar USER", width=10,command=lambda:self.ReadDataUser())
        self.botonReadUSER.grid(row=5, column=1, padx=10, pady=10)

        self.botonUpdate = Button(self.miFrame_2, text="Actualizar", width=10,command=lambda:self.updateData())
        self.botonUpdate.grid(row=4, column=2, padx=10, pady=10)

        self.botonDelete = Button(self.miFrame_2, text="Borrar", width=8,command=lambda:self.deleteData())
        self.botonDelete.grid(row=4, column=3, padx=10, pady=10)

        self.botonLimpiar = Button(self.miFrame_2, text="Limpiar", width=8,command=lambda:self.borrarInputBox())
        self.botonLimpiar.grid(row=5, column=0, padx=10, pady=10)

    #-----------------FUNCIONES-----------------------

    def UpdateTreeViewClientes(self):
        for row in self.treeVentas.get_children():
            self.treeVentas.delete(row)
        for row in self.consultarClientes():
            self.treeVentas.insert('',END, values=row)

    def consultarClientes(self):
        miConexion = sqlite3.connect("CLIENTES")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM CLIENTES")
        listamiCursor=miCursor.fetchall() #recuperar los datos
        arreglo = []
        for ventas in listamiCursor:
            arreglo.append(ventas)
        miCursor.close()
        return arreglo

    def crearDB(self):
        self.crearDB_Clientes()
        self.crearDB_ventas()

    def crearDB_Clientes(self):
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

    def crearDB_ventas(self):
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


    def leerInfoInputBox(self):
        #listadata = [self.datacuadroNombre.get(),self.datacuadroTelefono.get(), self.cuadroComentario.get('1.0', 'end')
        #        ]
        listadata = [self.datacuadroNombre.get(),self.datacuadroTelefono.get()]
        return listadata


    def borrarInputBox(self):

        #self.dataCuadroID.set("")
        self.datacuadroNombre.set("")
        self.datacuadroTelefono.set("")
        #self.cuadroComentario.delete('1.0', 'end')
        print("ClientesApp_demo - Se borran todos los campos")

    def InsertarData(self):
        
        try:
            miConexion = sqlite3.connect("CLIENTES")
            miCursor = miConexion.cursor()
            print("Successfully Connected to SQLite")

            listadata=self.leerInfoInputBox()
            print (listadata)
            #count = miCursor.execute("INSERT INTO CLIENTES VALUES (NULL,?,?,?)", listadata)
            count = miCursor.execute("INSERT INTO CLIENTES VALUES (NULL,?,?)", listadata)

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

    def ReadDataUser(self):
        
        try:
            miConexion = sqlite3.connect("CLIENTES")
            miCursor = miConexion.cursor()
            sql_update_query = """SELECT * FROM CLIENTES WHERE NOMBRE_USUARIO = ?"""
            name=str(self.cuadroNombre.get())
            miCursor.execute(sql_update_query,(name,))
            listamiCursor=miCursor.fetchone() #recuperar los datos
            print (listamiCursor)
            if(len(listamiCursor)!=0):
                #self.dataCuadroID.set(listamiCursor[0])
                self.datacuadroNombre.set(listamiCursor[1])
                self.datacuadroTelefono.set(listamiCursor[2])
                #self.cuadroComentario.delete('1.0', 'end')
                #self.cuadroComentario.insert('1.0',listamiCursor[3])        
            else:
                self.borrarInputBox()    
            miConexion.commit()
            print("Record read successfully")
            miConexion.close()
        except:
            print("Failed to ReadData data into sqlite table")
        finally:
            if (miConexion):
                miConexion.close()
                print("The SQLite connection is closed")

    def ReadDataID(self):
        
        try:
            miConexion = sqlite3.connect("CLIENTES")
            miCursor = miConexion.cursor()
            sql_update_query = """SELECT * FROM CLIENTES WHERE ID = ?"""
            name=int(self.cuadroID.get())
            miCursor.execute(sql_update_query,(name,))
            listamiCursor=miCursor.fetchone() #recuperar los datos
            if(len(listamiCursor)!=0):
                #self.dataCuadroID.set(listamiCursor[0])
                self.datacuadroNombre.set(listamiCursor[1])
                self.datacuadroTelefono.set(listamiCursor[2])
                #self.cuadroComentario.delete('1.0', 'end')
                #self.cuadroComentario.insert('1.0',listamiCursor[3])        
            else:
                self.borrarInputBox()    
            miConexion.commit()
            print("Record read successfully")
            miConexion.close()
        except:
            print("Failed to ReadData data into sqlite table")
        finally:
            if (miConexion):
                miConexion.close()
                print("The SQLite connection is closed")


    def updateData(self):
        
        try:    
            miConexion = sqlite3.connect("CLIENTES")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM CLIENTES")
            listamiCursor=miCursor.fetchall() #recuperar los datos
            IDleido=self.dataCuadroID.get()
            
            for datos in listamiCursor:
                if (datos[0]==int(IDleido)):            
                    data= self.leerInfoInputBox()
                    data.append(IDleido)

            #sql_update_query = """UPDATE CLIENTES set NOMBRE_USUARIO = ? ,TELEFONO = ?,COMENTARIOS = ? where ID = ?"""
            sql_update_query = """UPDATE CLIENTES set NOMBRE_USUARIO = ? ,TELEFONO = ? where ID = ?"""
            
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



    def deleteData(self):

        try:
            miConexion = sqlite3.connect("CLIENTES")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM CLIENTES")
            listamiCursor=miCursor.fetchall() #recuperar los datos
            IDleido=self.dataCuadroID.get()
            for datos in listamiCursor:
                if (datos[0]==int(IDleido)):
                    miCursor.execute("DELETE FROM CLIENTES WHERE ID=" + IDleido)
            self.borrarInputBox()
            miConexion.commit()
            print("Record delete successfully")
            miConexion.close()
        except:
            print("Failed to deleteData data into sqlite table")
        finally:
            if (miConexion):
                miConexion.close()
                print("The SQLite connection is closed")


class VentasFrame(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.miFrame_3 = Frame(self)
        self.miFrame_3.pack()

        self.tituloLabel=Label(self.miFrame_3,text="Ventas",fg="blue",bg="white",font=("Times New Roman",20))
        self.tituloLabel.grid(row=0, column=1, padx=10, pady=10,sticky="we")

        self.treeVentas = ttk.Treeview(self.miFrame_3,columns = ("ID_VENTAS","ID_USUARIO","DESCRIPCION","TOTAL_VENTA","DESCUENTO"))   
        self.treeVentas.grid(row=1,column=1,padx=10,pady=10)
        self.treeVentas['show']='headings'
        self.treeVentas.heading('#0', text='column0', anchor=tk.W)
        self.treeVentas.heading('#1', text='ID_VENTAS', anchor=tk.W)
        self.treeVentas.heading('#2', text='ID_USUARIO', anchor=tk.W)
        self.treeVentas.heading('#3', text='DESCRIPCION', anchor=tk.W)
        self.treeVentas.heading('#4', text='TOTAL_VENTA', anchor=tk.W)
        self.treeVentas.heading('#5', text='DESCUENTO', anchor=tk.W)

        self.treeVentas.column('#0',width=90,minwidth=90,stretch=tk.YES)
        self.treeVentas.column('#1',width=90,minwidth=90,stretch=tk.YES)
        self.treeVentas.column('#2',width=90,minwidth=90,stretch=tk.YES)
        self.treeVentas.column('#3',width=90,minwidth=90,stretch=tk.YES)
        self.treeVentas.column('#4',width=90,minwidth=90,stretch=tk.YES)
        self.treeVentas.column('#5',width=90,minwidth=90,stretch=tk.YES)
   
        for row in self.consultarVentas():
            self.treeVentas.insert('',END, values=row)

        self.scrollVert2=Scrollbar(self.miFrame_3,command=self.treeVentas.yview)
        self.scrollVert2.grid(row=1,column=2,sticky="nsnew")
        self.treeVentas.config(yscrollcommand=self.scrollVert2.set)


    def UpdateTreeViewVentas(self):
        for row in self.treeVentas.get_children():
            self.treeVentas.delete(row)
        for row in self.consultarVentas():
            self.treeVentas.insert('',END, values=row)

    def consultarVentas(self):
        miConexion = sqlite3.connect("VENTAS")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM VENTAS")
        listamiCursor=miCursor.fetchall() #recuperar los datos
        arreglo = []
        for ventas in listamiCursor:
            arreglo.append(ventas)
        miCursor.close()
        return arreglo

    def consultarVentasporClientes(self,id_usuario):
        cnx = self.conectar()
        cursor = cnx.cursor()
        sql_qry="""SELECT * FROM ventas WHERE ID_USUARIO = %s"""
        cursor.execute(sql_qry,(id_usuario,))

        arreglo = cursor.fetchall()
        self.CerrarConexion(cnx)
        return arreglo


class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("ClientesApp - Gestion Clientes-Ventas PL")
        
        self.notebook = ttk.Notebook(self)
        
        self.greeting_frame = ClientesFrame(self.notebook)
        self.notebook.add(
            self.greeting_frame, text="Clientes", padding=10)
        
        self.about_frame = VentasFrame(self.notebook)
        self.notebook.add(
            self.about_frame, text="Ventas", padding=10)
        
        self.notebook.pack(padx=10, pady=10)
        self.pack()

main_window = tk.Tk()
app = Application(main_window)
app.mainloop()