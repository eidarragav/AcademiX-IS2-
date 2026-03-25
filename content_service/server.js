
require('dotenv').config();

const express = require('express');
const connectDB = require('./src/config/db');

const app = express();

connectDB();

app.use(express.json());

app.use('/api/modules', require('./src/routes/moduleRoute'));
app.use('/api/lessons', require('./src/routes/lessonRoute'));


const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});