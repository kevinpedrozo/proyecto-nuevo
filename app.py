from flask import Flask, render_template, request, session
from pymongo import MongoClient
import random
import os

app = Flask(__name__)
app.secret_key = "clave-super-secreta"

# ==========================
# CONEXIÓN A MONGODB
# ==========================
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["juego"]
jugadores = db["jugadores"]

# Verificar conexión
try:
    client.admin.command("ping")
    print("MongoDB conectado correctamente")
except Exception as e:
    print("Error de conexión:", e)

# ==========================
# RUTA PRINCIPAL
# ==========================
@app.route("/", methods=["GET", "POST"])
def index():

    if "numero" not in session:
        session["numero"] = random.randint(1, 100)

    if "veces" not in session:
        session["veces"] = 0

    mensaje = ""

    if request.method == "POST":

        try:
            intento = int(request.form["intento"])

            numero = session["numero"]

            veces_actual = int(session.get("veces", 0))
            veces_actual += 1

            session["veces"] = veces_actual

            if intento < numero:

                mensaje = "El número es MAYOR."

            elif intento > numero:

                mensaje = "El número es MENOR."

            else:

                nombre = request.form.get(
                    "nombre",
                    "Anónimo"
                )

                # Guardar ganador en MongoDB
                jugadores.insert_one({
                    "nombre": nombre,
                    "intentos": session["veces"]
                })

                mensaje = (
                    f"¡Adivinaste! {nombre} "
                    f"lo lograste en "
                    f"{session['veces']} oportunidades."
                )

                session["numero"] = random.randint(1, 100)
                session["veces"] = 0

        except ValueError:

            mensaje = "Ingresa un número válido."

    return render_template(
        "index.html",
        mensaje=mensaje
    )

# ==========================
# VER JUGADORES
# ==========================
@app.route("/jugadores")
def ver_jugadores():

    lista = list(
        jugadores.find(
            {},
            {"_id": 0}
        )
    )

    return {
        "jugadores": lista
    }

# ==========================
# EJECUTAR APP
# ==========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
