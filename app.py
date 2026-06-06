from flask import Flask, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# Conexión a MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["prueba"]
estudiantes = db["base-datos-sena"]

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    registro_exitoso = False
    mostrar_ver = False

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        documento = request.form["documento"]

        # Verificar si el documento ya existe
        existe = estudiantes.find_one({"documento": documento})

        if existe:
            mensaje = "El estudiante ya está registrado."
            mostrar_ver = True
        else:
            estudiantes.insert_one({
                "nombre": nombre,
                "correo": correo,
                "documento": documento
            })
            mensaje = "Estudiante registrado correctamente."
            registro_exitoso = True

    return render_template(
        "index.html",
        mensaje=mensaje,
        registro_exitoso=registro_exitoso,
        mostrar_ver=mostrar_ver
    )

@app.route("/estudiantes")
def ver_estudiantes():
    # Retornamos una lista simple para ver los datos
    lista = list(estudiantes.find({}, {"_id": 0}))
    return {"estudiantes": lista}

if __name__ == "__main__":
    app.run(debug=True)
