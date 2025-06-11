// src/controllers/auth.controller.js

export const login = (req, res) => {
    // Obtenemos el email y la password del cuerpo de la petición
    const { email, password } = req.body;

    // --- LÓGICA DE LOGIN (NO SEGURA, PARA PRESENTACIÓN) ---
    // Usuario y contraseña "hardcodeados" (fijos en el código)
    const validEmail = 'admin@botisur.cl';
    const validPassword = '1234';

    // Verificamos si los datos recibidos son los correctos
    if (email === validEmail && password === validPassword) {
        // Si son correctos, enviamos una respuesta de éxito (código 200)
        console.log(`Login exitoso para: ${email}`);
        res.status(200).json({
            message: 'Login exitoso',
            user: {
                name: 'Administrador BotiSur',
                email: validEmail
            }
        });
    } else {
        // Si son incorrectos, enviamos un error de "No Autorizado" (código 401)
        console.log(`Intento de login fallido para: ${email}`);
        res.status(401).json({
            message: 'Email o contraseña incorrectos'
        });
    }
};