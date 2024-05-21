import tkinter as tk
from tkinter import ttk, simpledialog
import customtkinter as ctk
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import tkinter.messagebox as tk_messagebox



Base = declarative_base()

class HABITACIONES(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = 'habitaciones'
    # Definición de las columnas de la tabla
    ID = Column(Integer, primary_key=True)
    TIPO = Column(String(15))
    COSTO = Column(Integer)

class REGISTROS(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = 'registros'
    # Definición de las columnas de la tabla
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

class ESTADIASAPP(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)


        self.title("REGISTRO DE ESTADIAS")
        # Conexión a la base de datos
        engine = create_engine('mysql+pymysql://root@localhost/tp_programacion3')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()


        #ETIQUETAS NRO DE HABITACION
        tk.Label(self, text="Nro. de Habitación:").grid(row=0, column=0, padx=5, pady=10)
        #CAJAS DE ENTRY DE NUMERO DE HABITACION
        self.entry_nro = tk.Entry(self)
        self.entry_nro.grid(row=0, column=1, padx=5, pady=10)


        #MOSTRAR TABLA DE HABITACIONES Y COSTOS
        self.tabla_habitaciones = ttk.Treeview(self, columns=("TIPO", "COSTO"), show="headings")
        self.tabla_habitaciones.heading("TIPO", text="TIPO")
        self.tabla_habitaciones.heading("COSTO", text="COSTO")
        self.tabla_habitaciones.grid(row=1, column=0, columnspan=2,sticky="nsew", padx=5, pady=5)

        # ETIQUETAS TABLA DE REGISTROS
        tk.Label(self, text="REGISTROS").grid(row=0, column=2, padx=1, pady=1)

        #MOSTRAR TABLA DE REGISTROS
        self.tabla_registros = ttk.Treeview(self, columns=("NRO", "TIPO", "COSTO", "DIAS", "PAGO", "SUBTOTAL",
                                                           "%DESCUENTO", "TOTAL"), show="headings")
        self.tabla_registros.heading("NRO", text="NRO")
        self.tabla_registros.heading("TIPO", text="TIPO")
        self.tabla_registros.heading("COSTO", text="COSTO")
        self.tabla_registros.heading("DIAS", text="DIAS")
        self.tabla_registros.heading("PAGO", text="PAGO")
        self.tabla_registros.heading("SUBTOTAL", text="SUBTOTAL")
        self.tabla_registros.heading("%DESCUENTO", text="%DESCUENTO")
        self.tabla_registros.heading("TOTAL", text="TOTAL")
        self.tabla_registros.grid(row=1, column=2, padx=1, pady=1)


        # ETIQUETAS DIAS
        tk.Label(self, text="Días:").grid(row=2, column=0, padx=10, pady=10)
        # ENTRY DIAS
        self.entry_dias = tk.Entry(self)
        self.entry_dias.grid(row=2, column=1, padx=10, pady=10)


        #radiobutton para forma de pago
        self.forma_de_pago = tk.StringVar()
        self.forma_de_pago.set("CREDITO") #se asigna la unidad que aparece al iniciar
        self.CREDITO_btn = tk.Radiobutton(self, text="CREDITO", variable=self.forma_de_pago, value="CREDITO")
        self.CREDITO_btn.grid(row=3, column=1, padx=5, pady=5)
        self.CONTADO_btn = tk.Radiobutton(self, text="CONTADO", variable=self.forma_de_pago, value="CONTADO")
        self.CONTADO_btn.grid(row=4, column=1, padx=5, pady=5)

        #BOTONES
        # Crear el botón de cargar
        self.cargar_boton = ctk.CTkButton(self, text="CARGAR", command=self.cargar)
        self.cargar_boton.grid(row=5, column=0, padx=10, pady=10)
        # Crear el botón de anular
        self.anular_boton = ctk.CTkButton(self, text="ANULAR", command=self.anular)
        self.anular_boton.grid(row=5, column=1, padx=10, pady=10)
        # Crear el botón de modificar
        self.modificar_boton = ctk.CTkButton(self, text="MODIFICAR", command=self.modificar)
        self.modificar_boton.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        # Crear el botón de finalizar estadia
        self.finalizar_boton = ctk.CTkButton(self, text="FINALIZAR ESTADIA", command=self.finalizar)
        self.finalizar_boton.grid(row=2, column=2, columnspan=2, padx=1, pady=1)

        self.cargar_datos_desde_db()

    # AQUI SE CARGAN LOS DATOS PARA LAS TABLAS
    def cargar_datos_desde_db(self):

        habitaciones = self.session.query(HABITACIONES).all()
        for habitacion in habitaciones:
            self.tabla_habitaciones.insert("", "end", values=(habitacion.TIPO, habitacion.COSTO))

        registros = self.session.query(REGISTROS).filter_by(ESTADO="EN CURSO").all() #FILTRADO PARA QUE SOLO LISTE LOS
        for registro in registros:                                                      #REGISTROS "EN CURSO"
            self.tabla_registros.insert("", "end", values=(registro.NUMERO, registro.TIPO, registro.COSTO,
                                                           registro.DIAS, registro.PAGO, registro.SUBTOTAL,
                                                           registro.DESCUENTO, registro.TOTAL))


    # FUNCION DE CARGAR UN REGISTRO DE ESTADIA
    def cargar(self):
        numero = int(self.entry_nro.get())
        self.consultar_estado(numero)
        dias = int(self.entry_dias.get())
        habitacion_seleccionada = self.tabla_habitaciones.focus()
        if numero>0 and dias>0:
            if habitacion_seleccionada:
                tipo_habitacion = self.tabla_habitaciones.item(habitacion_seleccionada)['values'][0]
                costo_habitacion = int(self.tabla_habitaciones.item(habitacion_seleccionada)['values'][1])
                subtotal = costo_habitacion * dias
                descuento = int(self.calcular_descuento(dias))
                total = int(subtotal-(subtotal*(descuento/100)))
                if self.forma_de_pago.get()=="CREDITO":
                    tipo_de_pago="CR"
                else:
                    tipo_de_pago="CO"

                # ESTO ES PARA REALIZAR EL REGISTRO EN LA BASE DE DATOS
                nuevo_registro= REGISTROS(NUMERO=numero,TIPO=tipo_habitacion,COSTO=costo_habitacion,DIAS=dias,PAGO=tipo_de_pago,
                                          SUBTOTAL=subtotal,DESCUENTO=descuento,TOTAL=total, ESTADO="EN CURSO")
                self.session.add(nuevo_registro)
                self.session.commit()

                self.tabla_registros.delete(*self.tabla_registros.get_children())
                registros = self.session.query(REGISTROS).filter_by(ESTADO="EN CURSO").all()
                for registro in registros:
                    self.tabla_registros.insert("", "end", values=(registro.NUMERO, registro.TIPO, registro.COSTO,
                                                                   registro.DIAS, registro.PAGO, registro.SUBTOTAL,
                                                                   registro.DESCUENTO, registro.TOTAL))

            else:
                tk.messagebox.showerror("Error", "SELECCIONE UN TIPO DE HABITACION")
        else:
            tk.messagebox.showerror("Error", "INGRESE UN NUMERO DE DIAS O HABITACION VALIDO")




    # SE CONSULTA EL ESTADO DE UNA HABITACION, Y SI ESTA EN CURSO LA FINALIZA Y VUELVE A ACTUALIZAR LAS TABLAS
    def consultar_estado(self,numero):
        consulta_registro = self.session.query(REGISTROS).filter_by(NUMERO=numero, ESTADO="EN CURSO").first()
        if consulta_registro:
            consulta_registro.ESTADO = "FINALIZADO"
            self.session.commit()
            self.tabla_registros.delete(*self.tabla_registros.get_children())  # SE ENCARGA DE LIMPIAR LA TABLA ANTES
                                                                                # DE CARGAR LOS NUEVOS REGISTRO

        registros = self.session.query(REGISTROS).filter_by(ESTADO="EN CURSO").all()  #VOLVEMOS A LISTAR POR QUE HUBO
        for registro in registros:                                       #MODIFICACIONES Y SOLO SE LISTAS LOS ESTADOS "EN CURSO"
            self.tabla_registros.insert("", "end", values=(registro.NUMERO, registro.TIPO, registro.COSTO,
                                                           registro.DIAS, registro.PAGO, registro.SUBTOTAL,
                                                           registro.DESCUENTO, registro.TOTAL))

        return




    # SE CALCULA LOS DESCUENTOS
    def calcular_descuento(self,dias):
        forma_pago = self.forma_de_pago.get()
        if forma_pago == "CREDITO" and dias > 5:
            descuento = 5
        elif forma_pago == "CREDITO" and dias <= 5:
            descuento = 0
        else:
            descuento = 10

        if dias > 10:
            descuento = descuento + 2
        else:
            descuento = descuento + 0

        return descuento

    def anular (self):
        registro_seleccionado = self.tabla_registros.focus()
        if registro_seleccionado:
            nro_registro = self.tabla_registros.item(registro_seleccionado)['values'][0]
            consulta_registro = self.session.query(REGISTROS).filter_by(NUMERO=nro_registro, ESTADO="EN CURSO").first()
            if consulta_registro:
                consulta_registro.ESTADO = "ANULADO"
                self.session.commit()
                self.tabla_registros.delete(*self.tabla_registros.get_children())  # SE ENCARGA DE LIMPIAR LA TABLA ANTES
                                                                                   # DE CARGAR LOS NUEVOS REGISTRO

            registros = self.session.query(REGISTROS).filter_by(ESTADO="EN CURSO").all()  # VOLVEMOS A LISTAR POR QUE HUBO
            for registro in registros:                                # MODIFICACIONES Y SOLO SE LISTAS LOS ESTADOS "EN CURSO"
                self.tabla_registros.insert("", "end", values=(registro.NUMERO, registro.TIPO, registro.COSTO,
                                                               registro.DIAS, registro.PAGO, registro.SUBTOTAL,
                                                               registro.DESCUENTO, registro.TOTAL))

        else:
            tk.messagebox.showerror("Error", "SELECCIONE UN REGISTRO")



    def modificar(self):
        registro_seleccionado = self.tabla_registros.focus()
        if registro_seleccionado:
            nro_registro = self.tabla_registros.item(registro_seleccionado)['values'][0]
            consulta_registro = self.session.query(REGISTROS).filter_by(NUMERO=nro_registro, ESTADO="EN CURSO").first()
            if consulta_registro:
                nueva_duracion = simpledialog.askinteger("Modificar Duración", "Ingrese la nueva duración en días:",
                                                         minvalue=1)
                if nueva_duracion:
                    costo = consulta_registro.COSTO
                    forma_pago = consulta_registro.PAGO
                    if forma_pago == "CR" and nueva_duracion > 5:      #mismos calculo que la funcion, pero no se usa esa funcion porque los dias se obtienen por medio del entry y la forma de pago lo mismo
                        descuento = 5
                    elif forma_pago == "CR" and nueva_duracion <= 5:
                        descuento = 0
                    else:
                        descuento = 10

                    if nueva_duracion > 10:
                        descuento = descuento + 2
                    else:
                        descuento = descuento + 0

                    consulta_registro.DESCUENTO = descuento
                    consulta_registro.DIAS = nueva_duracion
                    consulta_registro.SUBTOTAL = costo * nueva_duracion

                    consulta_registro.TOTAL = consulta_registro.SUBTOTAL - (consulta_registro.SUBTOTAL * (descuento / 100))
                    self.session.commit()

                    self.tabla_registros.delete(*self.tabla_registros.get_children())

                    registros = self.session.query(REGISTROS).filter_by(ESTADO="EN CURSO").all()  # VOLVEMOS A LISTAR POR QUE HUBO
                    for registro in registros:                                                       # MODIFICACIONES Y SOLO SE LISTAS LOS ESTADOS "EN CURSO"
                        self.tabla_registros.insert("", "end", values=(registro.NUMERO, registro.TIPO, registro.COSTO,
                                                                       registro.DIAS, registro.PAGO, registro.SUBTOTAL,
                                                                       registro.DESCUENTO, registro.TOTAL))
                else:
                    tk.messagebox.showerror("Error", "DIGITE LOS DIAS")
        else:
            tk.messagebox.showerror("Error", "SELECCIONE UN REGISTRO")

    def finalizar(self):

        registro_seleccionado = self.tabla_registros.focus()
        if registro_seleccionado:
            nro_registro = self.tabla_registros.item(registro_seleccionado)['values'][0]
            consulta_registro = self.session.query(REGISTROS).filter_by(NUMERO=nro_registro, ESTADO="EN CURSO").first()
            if consulta_registro:
                consulta_registro.ESTADO = "FINALIZADO"
                self.session.commit()
                self.tabla_registros.delete(*self.tabla_registros.get_children())  # SE ENCARGA DE LIMPIAR LA TABLA ANTES
                                                                                    # DE CARGAR LOS NUEVOS REGISTRO

            registros = self.session.query(REGISTROS).filter_by(ESTADO="EN CURSO").all()  # VOLVEMOS A LISTAR POR QUE HUBO
            for registro in registros:                                   # MODIFICACIONES Y SOLO SE LISTAS LOS ESTADOS "EN CURSO"
                self.tabla_registros.insert("", "end", values=(registro.NUMERO, registro.TIPO, registro.COSTO,
                                                               registro.DIAS, registro.PAGO, registro.SUBTOTAL,
                                                               registro.DESCUENTO, registro.TOTAL))

        else:
            tk.messagebox.showerror("Error", "SELECCIONE UN REGISTRO")



