from flask import Flask, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# ==========================
# CONEXIÓN A MONGODB
# ==========================
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["prueba"]
estudiantes = db["base-datos-sena"]

# ==========================
# FORMULARIO PRINCIPAL
# ==========================
@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    registro_exitoso = False # Variable inicializada en False

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        documento = request.form["documento"]

        # Verificar si ya existe el documento
        existe = estudiantes.find_one({"documento": documento})

        if existe:
            mensaje = "El estudiante ya está registrado"
            registro_exitoso = False
        else:
            estudiantes.insert_one({
                "nombre": nombre,
                "correo": correo,
                "documento": documento
            })
            mensaje = "Estudiante registrado correctamente"
            registro_exitoso = True # Cambia a True al guardar

    return render_template(
        "index.html",
        mensaje=mensaje,
        registro_exitoso=registro_exitoso # Pasamos la variable al HTML
    )

# ... (resto de tus funciones se mantienen igual)
