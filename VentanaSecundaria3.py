import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


class HABITACIONES(Base):
    __tablename__ = 'habitaciones'
    ID = Column(Integer, primary_key=True)
    TIPO = Column(String(15))
    COSTO = Column(Integer)


class REGISTROS(Base):
    __tablename__ = 'registros'
    IDREGISTROS = Column(Integer, primary_key=True)
    NUMERO = Column(Integer)
    TIPO = Column(String(15))
    COSTO = Column(Integer)
    DIAS = Column(Integer)
    PAGO = Column(String(2))
    SUBTOTAL = Column(Integer)
    DESCUENTO = Column(Integer)
    TOTAL = Column(Integer)
    ESTADO = Column(String(10))


class VentanaSecundaria3(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("LISTAR RESUMENES")

        # Conexión a la base de datos
        engine = create_engine('mysql+pymysql://root@localhost/tp_programacion3')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # ETIQUETAS: ELEGIR EL TIPO DE HABITACION EN EL DESPLEGABLE
        tk.Label(self, text="TIPO DE HABITACION").grid(row=0, column=0, padx=5, pady=10)

        # Desplegable:
        self.tipo_habitacion_combobox = ttk.Combobox(self)
        self.tipo_habitacion_combobox.grid(row=1, column=0, padx=5, pady=10, )

        # Botón para iniciar la consulta
        self.consultar_boton = ctk.CTkButton(self, text="Consultar", command=self.consultar_registros)
        self.consultar_boton.grid(row=2, column=0, padx=5, pady=10)

        # Etiquetas para mostrar los resultados
        tk.Label(self, text="Total Días:").grid(row=3, column=0, padx=5, pady=5)
        self.total_dias_label = tk.Label(self, text="0")
        self.total_dias_label.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Total Ingresos:").grid(row=4, column=0, padx=5, pady=5)
        self.total_ingresos_label = tk.Label(self, text="0")
        self.total_ingresos_label.grid(row=4, column=1, padx=5, pady=5)

        # esta guncion llena el combobox con los tipos de habitación desde la base de datos
        self.cargar_tipos_habitacion()

    def cargar_tipos_habitacion(self):
        tipos = self.session.query(HABITACIONES.TIPO).distinct().all()
        tipos_unicos = [tipo[0] for tipo in tipos]
        self.tipo_habitacion_combobox['values'] = tipos_unicos
        if tipos_unicos:
            self.tipo_habitacion_combobox.current(0)  # Establecer valor predeterminado

    def consultar_registros(self):
        tipo_seleccionado = self.tipo_habitacion_combobox.get()
        registros = self.session.query(REGISTROS).filter_by(TIPO=tipo_seleccionado, ESTADO="FINALIZADO").all()

        total_dias = sum(registro.DIAS for registro in registros)
        total_ingresos = sum(registro.TOTAL for registro in registros)

        # Actualizar etiquetas con los resultados
        self.total_dias_label.config(text=str(total_dias))
        self.total_ingresos_label.config(text=str(total_ingresos))

