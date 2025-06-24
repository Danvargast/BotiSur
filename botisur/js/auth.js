document.addEventListener('DOMContentLoaded', () => {
    const loggedOutView = document.getElementById('logged-out-view');
    const loggedInView = document.getElementById('logged-in-view');
    const userGreetingEl = document.getElementById('user-greeting');
    
    if (!loggedOutView || !loggedInView) return; // Si los elementos no existen en la página, no hacer nada

    const token = localStorage.getItem('accessToken');

    if (token) {
        // Usuario logueado
        loggedOutView.style.display = 'none';
        loggedInView.style.display = 'flex'; // Usar flex para alinear los elementos

        // Decodificar el token para obtener el nombre del usuario (sin validar firma, solo para UI)
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            // Asumimos que el email está en el campo 'sub'
            if (userGreetingEl) {
                 userGreetingEl.textContent = `Hola, ${payload.sub.split('@')[0]}`;
            }
        } catch(e) {
            console.error("Error decodificando el token:", e);
        }

        document.getElementById('logout-btn').addEventListener('click', () => {
            localStorage.removeItem('accessToken');
            alert('Has cerrado sesión.');
            window.location.reload();
        });

    } else {
        // Usuario no logueado
        loggedOutView.style.display = 'flex';
        loggedInView.style.display = 'none';
    }
});
