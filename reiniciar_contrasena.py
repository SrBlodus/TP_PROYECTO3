import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    estado = Column(String(9), nullable=False)

class reiniciar_contrasena(tk.Toplevel):
    def __init__(self, parent, username_registro):
        super().__init__(parent)
        self.title("Cambiar Contraseña")

        # Conexión a la base de datos
        engine = create_engine('mysql+pymysql://root@localhost/tp_programacion3')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Guardar el nombre de usuario
        self.username = username_registro

        # ETIQUETAS
        tk.Label(self, text="Nueva Contraseña: ").grid(row=0, column=0, padx=5, pady=10)
        tk.Label(self, text="Confirmar Contraseña: ").grid(row=1, column=0, padx=5, pady=10)

        # ENTRYS
        self.entry_nro1 = tk.Entry(self,show="*")
        self.entry_nro1.grid(row=0, column=1, padx=5, pady=10)
        self.entry_nro2 = tk.Entry(self,show="*")
        self.entry_nro2.grid(row=1, column=1, padx=5, pady=10)

        # Botón para confirmar el cambio de contraseña
        self.consultar_boton = tk.Button(self, text="Restablecer Contraseña", command=self.cambiar)
        self.consultar_boton.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    def cambiar(self):
        print("Cambiar contraseña")
        contraseña1 = self.entry_nro1.get()
        contraseña2 = self.entry_nro2.get()
        if contraseña1 == contraseña2:
            consulta_usuario = self.session.query(User).filter_by(username=self.username).first()
            if consulta_usuario:
                salt = bcrypt.gensalt()
                pepper = os.environ.get("PEPPER", "default_pepper")
                hashed_password = bcrypt.hashpw(contraseña1.encode() + pepper.encode(), salt)
                consulta_usuario.password = hashed_password.decode()
                self.session.commit()
                messagebox.showinfo("CONTRASEÑA", "Contraseña reiniciada exitosamente!")
                print("Cerrando ventana")
                self.destroy()  # Cierra la ventana después de cambiar la contraseña
                print("se ejecuta destroy")
            else:
                messagebox.showerror("Error", "El usuario no está en estado nuevo")
        else:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
