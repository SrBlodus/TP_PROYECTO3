import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt
import os
from main_user import show_main_menu  # Importa la función del menú principal para usuarios normales
from admin_user import show_main_menu_admin  # Importa la función del menú principal para admin
from cambiar_contrasena import cambiar_contrasena# Importa la función para cambiar contraseña

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

def verify_login(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user:
        pepper = os.environ.get("PEPPER", "default_pepper")
        if bcrypt.checkpw(password.encode() + pepper.encode(), user.password.encode()):
            return user
    return None

def login():
    username = username_entry.get()
    password = password_entry.get()

    user = verify_login(username, password)
    if user:
        if user.estado == "nuevo":
            messagebox.showwarning("Contraseña", "Tu contraseña ha expirado. Debes cambiarla antes de continuar.")
            cambiar_contrasena(app,username)  # Importa la función para cambiar contraseña
        elif user.estado == "inactivo":
            messagebox.showerror("Error", "Usuario inactivo")
            return
        else:
            messagebox.showinfo("Login", "Login exitoso!")
            app.destroy()  # Cierra la ventana de inicio de sesión
            if username == "admin":
                show_main_menu_admin()  # Muestra el menú principal para el admin
            else:
                show_main_menu()  # Muestra el menú principal para usuarios normales
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

app = tk.Tk()
app.title("Login")
app.geometry("300x200")

login_frame = tk.Frame(app)

tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=10, pady=10)

username_entry = tk.Entry(login_frame)
password_entry = tk.Entry(login_frame, show="*")

username_entry.grid(row=0, column=1, padx=10, pady=10)
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

login_frame.pack()

app.mainloop()
