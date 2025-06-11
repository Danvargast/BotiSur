// src/routes/auth.routes.js
import { Router } from 'express';
import { login } from '../controllers/auth.controller.js';

const router = Router();

// Cuando llegue una petición POST a /api/login, se ejecuta la función 'login'
router.post('/login', login);

export default router;  