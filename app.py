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

# Verificar conexión
try:
    client.admin.command("ping")
    print("MongoDB conectado correctamente")
except Exception as e:
    print("Error de conexión:", e)

# ==========================
# FORMULARIO PRINCIPAL
# ==========================
@app.route("/", methods=["GET", "POST"])
def index():

    mensaje = ""

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]
        documento = request.form["documento"]

        # Verificar si ya existe el documento
        existe = estudiantes.find_one({
            "documento": documento
        })

        if existe:

            mensaje = "El estudiante ya está registrado"

        else:

            estudiantes.insert_one({
                "nombre": nombre,
                "correo": correo,
                "documento": documento
            })

            mensaje = "Estudiante registrado correctamente"

    return render_template(
        "index.html",
        mensaje=mensaje
    )

# ==========================
# VER REGISTROS
# ==========================
@app.route("/estudiantes")
def ver_estudiantes():

    lista = list(
        estudiantes.find(
            {},
            {"_id": 0}
        )
    )

    return {
        "estudiantes": lista
    }

# ==========================
# PRUEBA DE CONEXIÓN
# ==========================
@app.route("/testmongo")
def testmongo():

    estudiantes.insert_one({
        "nombre": "Prueba",
        "correo": "prueba@correo.com",
        "documento": "0000"
    })

    return "MongoDB funcionando correctamente"

# ==========================
# INICIAR APP
# ==========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
