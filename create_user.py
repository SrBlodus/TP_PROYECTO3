import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt
import os

engine = create_engine('mysql+pymysql://root@localhost/tp_programacion3')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    estado = Column(String(9), nullable=False)

Base.metadata.create_all(engine)

class Crear_Usuario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Registrar usuario")
        self.geometry("700x300")

        login_frame = tk.Frame(self)

        tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=10, pady=10)

        # ENTRYS
        self.username_entry = tk.Entry(login_frame)
        self.password_entry = tk.Entry(login_frame, show="*")

        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # BOTONES
        register_button = tk.Button(login_frame, text="Registrar", command=self.register)
        register_button.grid(row=2, column=0, columnspan=2, pady=10)

        anular_button = tk.Button(login_frame, text="Anular", command=self.anular)
        anular_button.grid(row=3, column=0, columnspan=2, pady=10)

        reiniciar_button = tk.Button(login_frame, text="Reiniciar", command=self.reiniciar)
        reiniciar_button.grid(row=4, column=0, columnspan=2, pady=10)

        # ETIQUETAS TABLA DE USUARIOS
        tk.Label(login_frame, text="USUARIOS").grid(row=0, column=2, padx=10, pady=10)

        # MOSTRAR TABLA DE USUARIOS
        self.tabla_usuarios = ttk.Treeview(login_frame, columns=("USUARIO", "ESTADO"), show="headings")
        self.tabla_usuarios.heading("USUARIO", text="USUARIO")
        self.tabla_usuarios.heading("ESTADO", text="ESTADO")
        self.tabla_usuarios.grid(row=1, column=2, rowspan=4, padx=10, pady=10)

        self.cargar_datos_desde_db()

        login_frame.pack()

    def cargar_datos_desde_db(self):
        self.tabla_usuarios.delete(*self.tabla_usuarios.get_children())
        usuarios = session.query(User).all()
        for usuario in usuarios:
            self.tabla_usuarios.insert("", "end", values=(usuario.username, usuario.estado))

    def create_user(self, username, password):
        salt = bcrypt.gensalt()
        pepper = os.environ.get("PEPPER", "default_pepper")
        hashed_password = bcrypt.hashpw(password.encode() + pepper.encode(), salt)
        new_user = User(username=username, password=hashed_password.decode(), salt=salt.decode(), estado='nuevo')
        session.add(new_user)
        session.commit()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            # Verificar si el usuario ya existe
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                messagebox.showerror("Error", "El nombre de usuario ya está en uso")
            else:
                self.create_user(username, password)
                messagebox.showinfo("Registro", "Usuario creado exitosamente!")
                self.destroy()  # Cierra la ventana después de registrar
        else:
            messagebox.showerror("Error", "Por favor, complete ambos campos")


    def anular(self):
        usuario_seleccionado = self.tabla_usuarios.focus()
        if usuario_seleccionado:
            username_registro = self.tabla_usuarios.item(usuario_seleccionado)['values'][0]
            consulta_usuario = session.query(User).filter_by(username=username_registro).first()
            if consulta_usuario:
                consulta_usuario.estado = "inactivo"
                session.commit()
                self.cargar_datos_desde_db()
            else:
                messagebox.showerror("Error", "No se encontró el usuario seleccionado")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un usuario")

    def reiniciar(self):
        usuario_seleccionado = self.tabla_usuarios.focus()
        if usuario_seleccionado:
            username_registro = self.tabla_usuarios.item(usuario_seleccionado)['values'][0]
            consulta_usuario = session.query(User).filter_by(username=username_registro).first()
            if consulta_usuario:
                consulta_usuario.estado = "nuevo"
                session.commit()
                self.cargar_datos_desde_db()
            else:
                messagebox.showerror("Error", "No se encontró el usuario seleccionado")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un usuario")

