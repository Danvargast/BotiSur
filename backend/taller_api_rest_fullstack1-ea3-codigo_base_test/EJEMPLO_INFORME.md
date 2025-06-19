# Informe de Microservicio -  (Coloque el nombre de su proyecto)

## Información General del Proyecto

(Para cada microservicio)
**Nombre del proyecto:** Gestión de Productos  
**Estudiantes:** [Nombre del estudiante]  
**Fecha de entrega:** [Fecha]  
**Rama del repositorio de Git:** [URL del repositorio]  

---

## 1. Descripción del Microservicio (Por ejemplo el de producto)

### 1.1 Propósito y Funcionalidad
Este microservicio está diseñado para gestionar un catálogo de productos dentro de un sistema de e-commerce. Permite realizar operaciones CRUD completas sobre los productos, incluyendo búsquedas especializadas por categoría.

### 1.2 Dominio de Negocio
El microservicio maneja la entidad `Product` que representa productos con atributos como nombre, categoría, precio y descripción. Es fundamental para sistemas de venta online, inventarios y catálogos digitales.

### 1.3 Integración con el Sistema General
Este microservicio se integra con otros componentes del sistema:
- **Microservicio de Inventario:** Para consultar disponibilidad de stock
- **Microservicio de Ventas:** Para procesar compras y actualizar información de productos
- **Microservicio de Usuarios:** Para gestionar favoritos y recomendaciones

---

## 2. Arquitectura y Diseño Técnico

### 2.1 Arquitectura MVC Implementada

El proyecto sigue el patrón **Modelo-Vista-Controlador (MVC)** adaptado para API REST:

```
├── controller/
│   └── ProductController.java    (Capa de Presentación/Control)
├── model/
│   └── Product.java             (Capa de Modelo/Entidad)
├── repository/
│   └── ProductRepository.java   (Capa de Acceso a Datos)
└── RestapiApplication.java      (Punto de entrada)
```

### 2.2 Separación de Responsabilidades

- **Controller (ProductController):** Maneja las peticiones HTTP, valida datos de entrada y retorna respuestas apropiadas
- **Model (Product):** Define la estructura de datos y mapeo con la base de datos usando JPA
- **Repository (ProductRepository):** Abstrae el acceso a datos y operaciones de persistencia

### 2.3 Tecnologías Utilizadas

- **Spring Boot 3.x:** Framework principal para desarrollo de aplicaciones Java
- **Spring Data JPA:** Para mapeo objeto-relacional y operaciones de base de datos
- **PostgreSQL:** Base de datos relacional alojada en Supabase
- **Maven:** Gestión de dependencias y ciclo de vida del proyecto
- **Hibernate:** Implementación JPA para ORM

---

## 3. Configuración del Proyecto

### 3.1 Configuración de Maven (pom.xml)

**Dependencias principales utilizadas:**
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>
```

### 3.2 Configuración de Base de Datos (application.properties)

```properties
spring.datasource.url=jdbc:postgresql://[supabase-url]:5432/postgres
spring.datasource.username=[username]
spring.datasource.password=[password]
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
```

### 3.3 Configuración de Supabase

**Pasos de configuración realizados:**
1. Creación de proyecto en Supabase
2. Configuración de tabla `products` con estructura apropiada
3. Configuración de credenciales de conexión
4. Pruebas de conectividad desde Spring Boot

---

## 4. Implementación del Modelo de Datos

### 4.1 Entidad Product

La entidad `Product` representa el modelo de datos principal con los siguientes atributos:

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | int | @Id, @GeneratedValue | Identificador único autogenerado |
| nombre | String | @Column(nullable = false) | Nombre del producto |
| categoria | String | @Column(nullable = false) | Categoría del producto |
| precio | double | @Column(nullable = false) | Precio del producto |
| descripcion | String | @Column(length = 1000) | Descripción detallada |

### 4.2 Mapeo JPA

```java
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    // ... otros campos
}
```

**Estrategias implementadas:**
- **GenerationType.IDENTITY:** Para autogeneración de IDs
- **@Column annotations:** Para definir restricciones de base de datos
- **@Table:** Para mapeo explícito con tabla de BD

---

## 5. API REST - Endpoints Implementados

### 5.1 Documentación de Endpoints

| Método | Endpoint | Descripción | Código de Respuesta |
|--------|----------|-------------|-------------------|
| POST | `/api/v1/product` | Crear nuevo producto | 201 Created |
| GET | `/api/v1/products` | Listar todos los productos | 200 OK |
| GET | `/api/v1/product/{id}` | Obtener producto por ID | 200 OK / 404 Not Found |
| GET | `/api/v1/products/categoria/{categoria}` | Buscar por categoría | 200 OK |
| PUT | `/api/v1/product/{id}` | Actualizar producto | 200 OK / 404 Not Found |
| DELETE | `/api/v1/product/{id}` | Eliminar producto | 204 No Content / 404 Not Found |

### 5.2 Ejemplos de Uso

**Crear Producto (POST):**
```json
{
    "nombre": "Laptop Gaming",
    "categoria": "Tecnología",
    "precio": 1299.99,
    "descripcion": "Laptop para gaming de alta gama"
}
```

**Respuesta de éxito:**
```json
{
    "id": 1,
    "nombre": "Laptop Gaming",
    "categoria": "Tecnología", 
    "precio": 1299.99,
    "descripcion": "Laptop para gaming de alta gama"
}
```

### 5.3 Manejo de Errores

El controlador implementa manejo apropiado de errores:
- **404 Not Found:** Cuando no se encuentra un producto por ID
- **201 Created:** Para creación exitosa de productos
- **204 No Content:** Para eliminación exitosa
- **200 OK:** Para operaciones de consulta y actualización exitosas

---

## 6. Pruebas con ThunderClient

### 6.1 Configuración de Pruebas

**Colección de pruebas creada con los siguientes casos:**

1. **Crear Producto:** Verificar creación exitosa y respuesta 201
2. **Listar Productos:** Confirmar listado completo y respuesta 200
3. **Buscar por ID:** Probar con ID existente y no existente
4. **Buscar por Categoría:** Filtrar productos por categoría específica
5. **Actualizar Producto:** Modificar datos existentes
6. **Eliminar Producto:** Remover producto del sistema

### 6.2 Resultados de Pruebas

| Endpoint | Estado | Tiempo Respuesta | Observaciones |
|----------|---------|------------------|---------------|
| POST /product |  Exitoso | 245ms | Producto creado correctamente |
| GET /products |  Exitoso | 189ms | Lista completa retornada |
| GET /product/1 |  Exitoso | 156ms | Producto encontrado |
| GET /product/999 |  Exitoso | 134ms | 404 retornado correctamente |
| PUT /product/1 |  Exitoso | 267ms | Actualización exitosa |
| DELETE /product/1 | Exitoso | 198ms | Eliminación exitosa |

### 6.3 Capturas de Pantalla

*[Aquí incluir capturas de pantalla de ThunderClient mostrando las pruebas exitosas]*

---

## 7. Control de Versiones con Git

### 7.1 Historial de Commits

**Estrategia de commits implementada:**
- Commits frecuentes con mensajes descriptivos
- Separación lógica de funcionalidades
- Uso de convenciones de naming

**Ejemplos de commits realizados:**
```
feat: Implementar entidad Product con anotaciones JPA
feat: Crear ProductRepository con métodos básicos  
feat: Desarrollar ProductController con CRUD completo
fix: Corregir mapeo de categoría en endpoint de búsqueda
docs: Agregar documentación de API endpoints
test: Validar endpoints con ThunderClient
refactor: Mejorar manejo de errores en controller
```

### 7.2 Estructura del Repositorio

```
microservicio-productos/
├── src/
│   └── main/
│       └── java/
│           └── com/profecarlos/tallerapirest/restapi/
├── pom.xml
├── README.md
└── .gitignore
```

### 7.3 Buenas Prácticas Git Aplicadas

- **README.md:** Documentación clara del proyecto
- **.gitignore:** Exclusión de archivos temporales y configuraciones sensibles
- **Commits atómicos:** Cada commit representa un cambio lógico específico
- **Mensajes descriptivos:** Siguiendo convención conventional commits

---

## 8. Buenas Prácticas Implementadas

### 8.1 Código Limpio

- **Nombres descriptivos:** Variables y métodos con nombres que expresan claramente su propósito
- **Métodos pequeños:** Cada método tiene una responsabilidad específica
- **Separación de concerns:** Clara división entre controller, model y repository

### 8.2 Arquitectura

- **Inyección de dependencias:** Uso de @Autowired para gestión automática
- **ResponseEntity:** Manejo apropiado de códigos de estado HTTP
- **Validation:** Uso de anotaciones JPA para validación de datos

### 8.3 Mantenibilidad

- **Estructura modular:** Fácil extensión y modificación
- **Convenciones Spring:** Seguimiento de estándares del framework
- **Documentación:** Código autodocumentado y comentarios donde es necesario

---

## 9. Desafíos y Soluciones

### 9.1 Configuración de Supabase

**Desafío:** Configurar correctamente la conexión con PostgreSQL en Supabase
**Solución:** Configuración detallada en application.properties y validación de credenciales

### 9.2 Manejo de Errores

**Desafío:** Implementar respuestas HTTP apropiadas para diferentes escenarios
**Solución:** Uso de Optional y map() para manejo elegante de casos de éxito y error

### 9.3 Consultas Personalizadas

**Desafío:** Implementar búsqueda por categoría
**Solución:** Método personalizado en repository usando convención de nombres JPA

---

## 10. Conclusiones y Aprendizajes

### 10.1 Logros Alcanzados

- ✅ CRUD completo funcional y probado
- ✅ Conexión exitosa con base de datos PostgreSQL
- ✅ API REST bien estructurada con códigos de estado apropiados
- ✅ Implementación de buenas prácticas de Spring Boot
- ✅ Control de versiones efectivo con Git

### 10.2 Conocimientos Adquiridos

- Comprensión profunda de arquitectura de microservicios
- Dominio de Spring Boot y Spring Data JPA
- Experiencia práctica con PostgreSQL y Supabase
- Habilidades de testing con ThunderClient
- Mejores prácticas de desarrollo colaborativo con Git

### 10.3 Posibles Mejoras Futuras

- Implementación de paginación para listado de productos
- Añadir validación de datos más robusta
- Implementar cache para mejorar rendimiento
- Agregar logging estructurado
- Implementar tests unitarios automatizados

---

## 11. Anexos

### 11.1 Configuración Completa

*[Incluir archivos de configuración relevantes]*

### 11.2 Evidencias de Funcionamiento

*[Capturas de pantalla de pruebas en ThunderClient]*

### 11.3 Estructura Final del Proyecto

*[Árbol de directorios del proyecto final]*

---

**Firma del estudiante:** [Nombre]  
**Fecha:** [Fecha de entrega]