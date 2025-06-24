// js/shop-logic.js

const API_URL = 'http://127.0.0.1:8000';

// --- CARGA DE PRODUCTOS ---
async function fetchYMostrarProductos() {
    const container = document.getElementById('productos-container');
    container.innerHTML = `<div class="col-12 producto-placeholder"><div class="spinner-border text-primary" role="status"><span class="sr-only">Cargando...</span></div><p class="mt-2">Cargando productos...</p></div>`;
    try {
        const response = await fetch(`${API_URL}/productos/`);
        if (!response.ok) throw new Error('No se pudo conectar al servidor.');
        
        const productos = await response.json();
        container.innerHTML = ''; 

        if (productos.length === 0) {
            container.innerHTML = '<div class="col-12 producto-placeholder"><p>No hay productos disponibles.</p></div>';
            return;
        }

        productos.forEach(producto => {
            const imageUrl = producto.imagen_url || `https://placehold.co/400x300/e8e8e8/666?text=${encodeURIComponent(producto.nombre)}`;
            const col = document.createElement('div');
            col.className = 'col mb-4';
            col.innerHTML = `
                <div class="card h-100">
                     <img src="${imageUrl}" class="card-img-top" alt="${producto.nombre}" onerror="this.onerror=null;this.src='https://placehold.co/400x300/e8e8e8/666?text=Imagen no disponible';">
                    <div class="card-body text-center d-flex flex-column">
                        <h5 class="card-title">${producto.nombre}</h5>
                        <p class="card-text mt-auto"><strong>$${parseFloat(producto.precio).toLocaleString('es-CL')}</strong></p>
                    </div>
                    <div class="card-footer text-center">
                        <button class="btn btn-primary" onclick='agregarAlCarrito(${JSON.stringify(producto)})'>Añadir al carrito</button>
                    </div>
                </div>
            `;
            container.appendChild(col);
        });
    } catch (error) {
        container.innerHTML = `<div class="col-12 producto-placeholder"><p>Error al cargar productos: ${error.message}</p></div>`;
    }
}

// --- LÓGICA DEL CARRITO ---
const getCarrito = () => JSON.parse(localStorage.getItem('botisur_carrito')) || [];
const saveCarrito = (carrito) => {
    localStorage.setItem('botisur_carrito', JSON.stringify(carrito));
    actualizarVistaCarrito();
};
const agregarAlCarrito = (producto) => {
    const carrito = getCarrito();
    const itemExistente = carrito.find(item => item.id_producto === producto.id_producto);
    if (itemExistente) { itemExistente.cantidad++; } else { carrito.push({ ...producto, cantidad: 1 }); }
    saveCarrito(carrito);
    abrirCarrito();
};
const eliminarDelCarrito = (productoId) => {
    let carrito = getCarrito();
    carrito = carrito.filter(item => item.id_producto !== productoId);
    saveCarrito(carrito);
};
const actualizarVistaCarrito = () => {
    const carrito = getCarrito();
    const listaEl = document.getElementById('carrito-lista');
    const totalEl = document.getElementById('carrito-total');
    const contadorEl = document.getElementById('carrito-contador');
    
    if (!listaEl || !totalEl || !contadorEl) return;

    listaEl.innerHTML = '';
    let totalGeneral = 0;
    let totalItems = 0;

    if (carrito.length === 0) {
        listaEl.innerHTML = '<li class="list-group-item text-center text-muted">Tu carrito está vacío.</li>';
        document.getElementById('pagar-btn').disabled = true;
    } else {
        document.getElementById('pagar-btn').disabled = false;
        carrito.forEach(item => {
            const itemTotal = item.precio * item.cantidad;
            totalGeneral += itemTotal;
            totalItems += item.cantidad;
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <div>${item.nombre} <br><small class="text-muted">${item.cantidad} x $${parseFloat(item.precio).toLocaleString('es-CL')}</small></div>
                <button class="btn btn-sm btn-outline-danger" onclick="eliminarDelCarrito(${item.id_producto})">&times;</button>
            `;
            listaEl.appendChild(li);
        });
    }
    
    totalEl.innerText = `$${totalGeneral.toLocaleString('es-CL')}`;
    contadorEl.innerText = totalItems;
};

// --- LÓGICA DE PAGO MEJORADA ---
function handlePagarClick() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        alert('Debes iniciar sesión para poder pagar.');
        window.location.href = 'login.html';
        return;
    }
    
    const carrito = getCarrito();
    if (carrito.length === 0) {
        alert('Tu carrito está vacío.');
        return;
    }

    const resumenLista = document.getElementById('resumen-pedido-lista');
    const resumenTotal = document.getElementById('resumen-pedido-total');
    resumenLista.innerHTML = '';
    let total = 0;

    carrito.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between lh-condensed';
        li.innerHTML = `
            <div>
                <h6 class="my-0">${item.nombre}</h6>
                <small class="text-muted">Cantidad: ${item.cantidad}</small>
            </div>
            <span class="text-muted">$${(item.precio * item.cantidad).toLocaleString('es-CL')}</span>`;
        resumenLista.appendChild(li);
        total += item.precio * item.cantidad;
    });

    resumenTotal.innerText = `$${total.toLocaleString('es-CL')}`;
    $('#confirmacionPagoModal').modal('show');
}

async function procesarVentaSimulada() {
    const token = localStorage.getItem('accessToken');
    const carrito = getCarrito();
    const detalles = carrito.map(item => ({ producto_id: item.id_producto, cantidad: item.cantidad }));
    const btnConfirmar = document.getElementById('confirmar-pago-btn');
    const spinner = btnConfirmar.querySelector('.spinner-border');

    btnConfirmar.disabled = true;
    spinner.style.display = 'inline-block';

    try {
        await new Promise(resolve => setTimeout(resolve, 1500)); 
        console.log("Enviando venta (simulado):", { detalles });
        
        alert('¡Compra realizada con éxito!');
        saveCarrito([]);
        cerrarCarrito();
        $('#confirmacionPagoModal').modal('hide');
    } catch (error) {
        alert(`Error simulado: ${error.message}`);
    } finally {
        btnConfirmar.disabled = false;
        spinner.style.display = 'none';
    }
}

// --- CONTROL UI CARRITO ---
const abrirCarrito = () => document.getElementById('carrito-panel').classList.add('abierto');
const cerrarCarrito = () => document.getElementById('carrito-panel').classList.remove('abierto');

// --- INICIALIZACIÓN ---
document.addEventListener('DOMContentLoaded', () => {
    // Solo ejecutar lógica de la tienda si estamos en la página correcta
    if (document.getElementById('productos-container')) {
        fetchYMostrarProductos();
        actualizarVistaCarrito();

        // **AQUÍ SE ASIGNAN LOS EVENTOS**
        // Si esta sección no se ejecuta, los botones no funcionarán.
        document.getElementById('pagar-btn').addEventListener('click', handlePagarClick);
        document.getElementById('carrito-toggle').addEventListener('click', abrirCarrito);
        document.getElementById('cerrar-carrito').addEventListener('click', cerrarCarrito); // <-- Este es el evento clave para el botón "x"
        document.getElementById('confirmar-pago-btn').addEventListener('click', procesarVentaSimulada);

        document.addEventListener('keydown', (e) => {
            if (e.key === "Escape" && document.getElementById('carrito-panel').classList.contains('abierto')) {
                cerrarCarrito();
            }
        });
    }
});