const express = require('express');
const mongoose = require('mongoose');
const app = express();

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));

// Conexión a tu base de datos (MongoDB Atlas)
mongoose.connect('mongodb+srv://kevin:rhLLyfdM3CTyhXBV@cluster0.oowbmus.mongodb.net/escuela');

// Definición del esquema (debe coincidir con lo que guardas)
const Estudiante = mongoose.model('Estudiante', { 
    nombre: String, 
    correo: String, 
    documento: String 
});

// CONSULTA: Aquí es donde traes los datos de la base de datos
app.get('/', async (req, res) => {
    try {
        const lista = await Estudiante.find(); // ESTA LÍNEA HACE LA MAGIA
        res.render('index', { estudiantes: lista, mensaje: null });
    } catch (err) {
        res.send("Error al consultar la base de datos");
    }
});

// GUARDAR: Cuando presionas el botón
app.post('/', async (req, res) => {
    await new Estudiante(req.body).save();
    const lista = await Estudiante.find();
    res.render('index', { estudiantes: lista, mensaje: "Guardado correctamente" });
});

app.listen(3000, () => console.log('Servidor en http://localhost:3000'));