import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import tkinter.messagebox as tk_messagebox

Base = declarative_base()


class HABITACIONES(Base):
    __tablename__ = 'habitaciones'
    ID = Column(Integer, primary_key=True)
    TIPO = Column(String(15))
    COSTO = Column(Integer)


class GestionHabitaciones(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Habitaciones")

        # Conexión a la base de datos
        engine = create_engine('mysql+pymysql://root@localhost/tp_programacion3')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Etiquetas y entradas para el tipo y el costo de la habitación
        tk.Label(self, text="Tipo de Habitación:").grid(row=0, column=0, padx=10, pady=10)
        self.tipo_habitacion_entry = tk.Entry(self)
        self.tipo_habitacion_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Costo de Habitación:").grid(row=1, column=0, padx=10, pady=10)
        self.costo_habitacion_entry = tk.Entry(self)
        self.costo_habitacion_entry.grid(row=1, column=1, padx=10, pady=10)

        # Botones para agregar y modificar habitaciones
        self.agregar_boton = ctk.CTkButton(self, text="Agregar Habitación", command=self.agregar_habitacion)
        self.agregar_boton.grid(row=2, column=0, padx=10, pady=10)

        self.modificar_boton = ctk.CTkButton(self, text="Modificar Habitación", command=self.modificar_habitacion)
        self.modificar_boton.grid(row=2, column=1, padx=10, pady=10)

        # Tabla para mostrar las habitaciones
        self.tabla_habitaciones = ttk.Treeview(self, columns=("ID", "TIPO", "COSTO"), show="headings")
        self.tabla_habitaciones.heading("ID", text="ID")
        self.tabla_habitaciones.heading("TIPO", text="TIPO")
        self.tabla_habitaciones.heading("COSTO", text="COSTO")
        self.tabla_habitaciones.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.tabla_habitaciones.bind("<<TreeviewSelect>>", self.seleccionar_habitacion)

        self.cargar_datos_desde_db()

    def cargar_datos_desde_db(self):
        for row in self.tabla_habitaciones.get_children():
            self.tabla_habitaciones.delete(row)
        habitaciones = self.session.query(HABITACIONES).all()
        for habitacion in habitaciones:
            self.tabla_habitaciones.insert("", "end", values=(habitacion.ID, habitacion.TIPO, habitacion.COSTO))

    def agregar_habitacion(self):
        tipo = self.tipo_habitacion_entry.get()
        costo = self.costo_habitacion_entry.get()
        if tipo and costo:
            try:
                costo = int(costo)
                nueva_habitacion = HABITACIONES(TIPO=tipo, COSTO=costo)
                self.session.add(nueva_habitacion)
                self.session.commit()
                self.cargar_datos_desde_db()
                self.tipo_habitacion_entry.delete(0, tk.END)
                self.costo_habitacion_entry.delete(0, tk.END)
            except ValueError:
                tk_messagebox.showerror("Error", "El costo debe ser un número entero")
        else:
            tk_messagebox.showerror("Error", "Todos los campos son obligatorios")

    def seleccionar_habitacion(self, event):
        habitacion_seleccionada = self.tabla_habitaciones.focus()
        if habitacion_seleccionada:
            item = self.tabla_habitaciones.item(habitacion_seleccionada)
            self.tipo_habitacion_entry.delete(0, tk.END)
            self.costo_habitacion_entry.delete(0, tk.END)
            self.tipo_habitacion_entry.insert(0, item["values"][1])
            self.costo_habitacion_entry.insert(0, item["values"][2])

    def modificar_habitacion(self):
        habitacion_seleccionada = self.tabla_habitaciones.focus()
        if habitacion_seleccionada:
            item = self.tabla_habitaciones.item(habitacion_seleccionada)
            id_habitacion = item["values"][0]
            nuevo_tipo = self.tipo_habitacion_entry.get()
            nuevo_costo = self.costo_habitacion_entry.get()
            if nuevo_tipo and nuevo_costo:
                try:
                    nuevo_costo = int(nuevo_costo)
                    habitacion = self.session.query(HABITACIONES).filter_by(ID=id_habitacion).first()
                    if habitacion:
                        habitacion.TIPO = nuevo_tipo
                        habitacion.COSTO = nuevo_costo
                        self.session.commit()
                        self.cargar_datos_desde_db()
                        self.tipo_habitacion_entry.delete(0, tk.END)
                        self.costo_habitacion_entry.delete(0, tk.END)
                except ValueError:
                    tk_messagebox.showerror("Error", "El costo debe ser un número entero")
            else:
                tk_messagebox.showerror("Error", "Todos los campos son obligatorios")
        else:
            tk_messagebox.showerror("Error", "Seleccione una habitación de la lista")


