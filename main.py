import tkinter as tk
import customtkinter as ctk
from VentanaSecundaria1 import GestionHabitaciones
from VentanaSecundaria2 import ESTADIASAPP
from VentanaSecundaria3 import VentanaSecundaria3

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("ADMINISTRACION DE ESTADIAS")

        self.mostrar_ventana1_boton = tk.Button(self, text="MODIFICACION DE ESTADIAS Y COSTO DIARIO", command=self.mostrar_segunda_ventana1)
        self.mostrar_ventana1_boton.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.mostrar_ventana2_boton = tk.Button(self, text="REGISTRAR ESTADIAS",command=self.mostrar_segunda_ventana2)
        self.mostrar_ventana2_boton.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.mostrar_ventana3_boton = tk.Button(self, text="LISTAR", command=self.mostrar_tercera_ventana2)
        self.mostrar_ventana3_boton.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def mostrar_segunda_ventana1(self):
        segunda_ventana = GestionHabitaciones(self)
        segunda_ventana.transient(self)
        segunda_ventana.grab_set()
        self.wait_window(segunda_ventana)

    def mostrar_segunda_ventana2(self):
        segunda_ventana = ESTADIASAPP(self)
        segunda_ventana.transient(self)
        segunda_ventana.grab_set()
        self.wait_window(segunda_ventana)

    def mostrar_tercera_ventana2(self):
        tercera_ventana = VentanaSecundaria3(self)
        tercera_ventana.transient(self)
        tercera_ventana.grab_set()
        self.wait_window(tercera_ventana)

if __name__ == "__main__":
    app = App()

    app.mainloop()
