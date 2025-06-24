// js/auth.js - Versión mejorada

/**
 * Esta función se ejecuta en cada carga de página.
 * Verifica si hay un token, comprueba su validez con el backend
 * y actualiza la UI para mostrar el estado correcto (logueado o no).
 */
document.addEventListener('DOMContentLoaded', async () => {
    const authContainer = document.getElementById('auth-container');
    const token = localStorage.getItem('accessToken');

    if (!authContainer) {
        // Si la página no tiene el contenedor de autenticación, no hace nada.
        return;
    }

    if (token) {
        // Si encontramos un token, intentamos verificarlo con el backend.
        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                // El token es válido. Obtenemos los datos del usuario.
                const user = await response.json();
                renderLoggedInView(authContainer, user);
            } else {
                // El token es inválido o ha expirado.
                logout(authContainer);
            }
        } catch (error) {
            // Error de red o el backend no responde.
            console.error('Error al verificar el token:', error);
            renderLoggedOutView(authContainer);
        }
    } else {
        // No hay token, mostramos la vista de "desconectado".
        renderLoggedOutView(authContainer);
    }
});

/**
 * Muestra la vista para un usuario que ha iniciado sesión.
 * @param {HTMLElement} container - El div #auth-container.
 * @param {object} user - El objeto de usuario con 'nombre'.
 */
function renderLoggedInView(container, user) {
    // Mostramos un saludo y el botón de cerrar sesión.
    container.innerHTML = `
        <span class="navbar-text mr-3">
            Hola, ${user.nombre}
        </span>
        <button id="logout-btn" class="btn btn-outline-danger">Cerrar Sesión</button>
    `;

    // Añadimos el evento al botón de cerrar sesión.
    document.getElementById('logout-btn').addEventListener('click', () => {
        logout(container);
    });
}

/**
 * Muestra la vista para un usuario que no ha iniciado sesión.
 * @param {HTMLElement} container - El div #auth-container.
 */
function renderLoggedOutView(container) {
    container.innerHTML = `
        <a href="registro.html" class="btn btn-outline-primary mr-2">Registrarse</a>
        <a href="login.html" class="btn btn-primary">Iniciar Sesión</a>
    `;
}

/**
 * Limpia los datos de la sesión del navegador y recarga la página.
 */
function logout() {
    localStorage.removeItem('accessToken');
    alert('Has cerrado la sesión.');
    window.location.reload(); // Recarga la página para asegurar que todo se actualice.
}