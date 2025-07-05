¡Excelente\! Con toda esta información, puedo generar una versión actualizada y completa de tu archivo `README.md` que cumple con las pautas de tu evaluación.

Aquí tienes la propuesta. He reestructurado y enriquecido el contenido basándome en los archivos de tu proyecto y tus respuestas.

-----

# Botillería BotiSur :beer:

Repositorio oficial del proyecto BotiSur, un sistema de pedidos y delivery para una botillería online.

## :speech\_balloon: Descripción del Proyecto

**BotiSur** es una aplicación web que cuenta con un backend desarrollado en **FastAPI** para gestionar una botillería online. El sistema permite a los usuarios registrarse, iniciar sesión, explorar un catálogo de productos, y realizar compras. Además, incluye una funcionalidad especial que se conecta a una API externa ([TheCocktailDB](https://www.thecocktaildb.com/)) para buscar y mostrar recetas de cócteles según el ingrediente que elija el usuario.

[cite\_start]El backend se encarga de toda la lógica de negocio, incluyendo la autenticación de usuarios mediante tokens JWT, la gestión de inventario, y el procesamiento de ventas[cite: 1]. La información se almacena en una base de datos **PostgreSQL** gestionada a través de **Supabase**.

-----

## :busts\_in\_silhouette: Integrantes del Equipo

  * **Líder de Equipo:** Daniel Vargas
  * **Desarrollador Frontend:** Yeisson Thomas
  * **Desarrollador Backend:** Alvaro Oyarzun
  * **Diseñador UI/UX:** Rodrigo Ruiz

-----

## :computer: Tecnologías Utilizadas

| Área | Tecnología |
| :--- | :--- |
| **Backend** | Python, FastAPI, SQLAlchemy, Uvicorn |
| **Base de Datos** | PostgreSQL (Supabase) |
| **Frontend** | HTML, CSS, JavaScript |
| **Autenticación** | python-jose (JWT), passlib (bcrypt) |
| **Herramientas** | Git, GitHub, Visual Studio Code |

-----

## :rocket: Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### **1. Prerrequisitos**

Asegúrate de tener instalado el siguiente software:

  * [Git](https://git-scm.com/)
  * [Python 3.9](https://www.python.org/downloads/) o superior
  * [Visual Studio Code](https://code.visualstudio.com/)
  * La extensión **Live Server** en VS Code.

### **2. Clonar el Repositorio**

```bash
git clone https://github.com/Danvargast/BotiSur.git
cd BotiSur
```

### **3. Configurar el Backend**

1.  **Crear el archivo de entorno:**

      * Dentro de la carpeta del proyecto, crea un archivo llamado `.env`.
      * Añade las credenciales de tu base de datos de Supabase. El archivo debe tener la siguiente estructura:

    <!-- end list -->

    ```env
    DATABASE_URL="postgresql://user:password@host:port/dbname"
    SECRET_KEY="tu_clave_secreta_para_jwt"
    ```

2.  **Crear y activar un entorno virtual:**

      * Navega a la carpeta del proyecto en tu terminal.
      * Crea el entorno:
        ```bash
        python -m venv venv
        ```
      * Activa el entorno:
          * **Windows:** `.\venv\Scripts\activate`
          * **macOS/Linux:** `source venv/bin/activate`

3.  **Instalar dependencias:**

      * Asegúrate de que el entorno virtual esté activado.
      * Ejecuta el siguiente comando para instalar las librerías de Python:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Iniciar el servidor del backend:**

      * Con el entorno virtual activado, ejecuta:
        ```bash
        uvicorn main:app --reload
        ```
      * El backend estará funcionando en `http://127.0.0.1:8000`. No cierres esta terminal.

### **4. Ejecutar el Frontend**

1.  Abre la carpeta del proyecto en Visual Studio Code.
2.  Haz clic derecho sobre el archivo `index.html` (o cualquier otra vista como `login.html`).
3.  Selecciona la opción **"Open with Live Server"**.
4.  Tu navegador se abrirá automáticamente con la página web funcionando.

-----

## :link: Enlace al Despliegue

Puedes acceder a la versión en producción del proyecto a través del siguiente enlace:

> **[Enlace al sitio web]** (Aquí debes pegar el enlace cuando lo tengas desplegado)

-----

## :page\_facing\_up: Licencia

Este proyecto está bajo la [Licencia MIT](https://opensource.org/licenses/MIT).

-----

## :email: Contacto

Para cualquier duda o consulta, puedes contactar a `dan.vargast@duocuc.cl`.
