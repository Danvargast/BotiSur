// js/recetas-logic.js

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const ingredientInput = document.getElementById('ingredient-input');
    const resultsContainer = document.getElementById('results-container');

    if (!searchForm) return; // Si no estamos en la página de recetas, no hacer nada.

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Evita que el formulario recargue la página.
        
        const ingrediente = ingredientInput.value.trim();
        if (!ingrediente) {
            alert('Por favor, ingresa un ingrediente.');
            return;
        }

        renderLoading(); // Muestra un indicador de carga.

        try {
            // Llama a nuestra propia API de backend
            const response = await fetch(`${API_URL}/recetas/${ingrediente}`);
            
            if (!response.ok) {
                throw new Error('No se pudo obtener la información. Inténtalo de nuevo.');
            }

            const recetas = await response.json();
            renderResults(recetas); // Muestra los resultados.

        } catch (error) {
            renderError(error.message); // Muestra un mensaje de error.
        }
    });

    /**
     * Muestra un estado de "Cargando..." en el contenedor de resultados.
     */
    function renderLoading() {
        resultsContainer.innerHTML = `
            <div class="col-12 text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="sr-only">Cargando...</span>
                </div>
                <p class="mt-2">Buscando recetas...</p>
            </div>
        `;
    }

    /**
     * Muestra un mensaje de error en el contenedor de resultados.
     * @param {string} message - El mensaje de error a mostrar.
     */
    function renderError(message) {
        resultsContainer.innerHTML = `
            <div class="col-12 text-center text-danger">
                <p><strong>Error:</strong> ${message}</p>
            </div>
        `;
    }

    /**
     * Renderiza las tarjetas de recetas en el contenedor.
     * @param {Array} recetas - Un array de objetos de receta.
     */
    function renderResults(recetas) {
        resultsContainer.innerHTML = ''; // Limpia el contenido anterior.

        if (recetas.length === 0) {
            resultsContainer.innerHTML = `
                <div class="col-12 text-center text-muted">
                    <p>No se encontraron recetas para "${ingredientInput.value}". Prueba con otro ingrediente.</p>
                </div>
            `;
            return;
        }

        recetas.forEach(receta => {
            const recipeCard = document.createElement('div');
            recipeCard.className = 'col-md-4 col-sm-6 mb-4';

            // Genera la lista de ingredientes para la tarjeta.
            const ingredientesHTML = receta.ingredientes
                .map(ing => `<li>${ing.nombre} <small class="text-muted">(${ing.medida || 'a gusto'})</small></li>`)
                .join('');

            recipeCard.innerHTML = `
                <div class="card h-100 recipe-card">
                    <img src="${receta.imagen_url}" class="card-img-top" alt="${receta.nombre}">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${receta.nombre}</h5>
                        <p><strong>Ingredientes:</strong></p>
                        <ul>${ingredientesHTML}</ul>
                        <p class="mt-auto"><strong>Instrucciones:</strong> ${receta.instrucciones.substring(0, 100)}...</p>
                    </div>
                </div>
            `;
            resultsContainer.appendChild(recipeCard);
        });
    }
});