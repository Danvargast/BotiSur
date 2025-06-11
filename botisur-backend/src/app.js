// src/app.js
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.routes.js';

// Cargar variables de entorno
dotenv.config();

const app = express();

// Configuraciones
app.set('port', process.env.PORT || 4000);

// Middlewares (funciones que se ejecutan antes de llegar a las rutas)
app.use(cors()); // Permite la comunicación entre dominios diferentes (frontend y backend)
app.use(express.json()); // Permite que el servidor entienda JSON

// Rutas
app.get('/', (req, res) => {
    res.send('Backend de BotiSur funcionando!');
});

app.use('/api', authRoutes);


export default app;