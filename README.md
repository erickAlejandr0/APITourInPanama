#  API Tour In Panama

API RESTful desarrollada con FastAPI para la gestión de actividades turísticas en Panamá. Permite a los usuarios descubrir actividades cercanas, gestionar itinerarios personalizados y compartir experiencias mediante un sistema de comentarios.

##  Descripción

Este proyecto proporciona una API  para aplicaciones móviles y web de turismo, ofreciendo funcionalidades como:

-  Autenticación y registro de usuarios
-  Búsqueda de actividades cercanas por ubicación geográfica
-  Gestión de itinerarios personalizados
-  Sistema de comentarios y valoraciones
-  Categorización de actividades turísticas
-  Limpieza automática de actividades expiradas mediante schedulers

##  Tecnologías

- **Framework:** FastAPI 0.115.13
- **Base de Datos:** PostgreSQL con Supabase
- **ORM/Cliente:** asyncpg 0.30.0
- **Servidor:** Uvicorn 0.34.3
- **Tareas programadas:** APScheduler 3.11.0
- **Validación:** Pydantic 2.11.7
- **CORS:** FastAPI Middleware

##  Estructura del Proyecto

```
APITourInPanama/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Punto de entrada de la aplicación
│   ├── dataBase/
│   │   ├── __init__.py
│   │   └── db.py                    # Configuración de conexión a BD
│   ├── Models/                      # Modelos Pydantic
│   │   ├── actividadesModel_out.py
│   │   ├── comentariosModel.py
│   │   ├── itinerarioModel.py
│   │   ├── itinerarioModeloOut.py
│   │   ├── perfilModel.py
│   │   └── userModel.py
│   ├── routers/                     # Endpoints de la API
│   │   ├── actividades.py
│   │   ├── perfiles.py
│   │   └── usuarios.py
│   ├── schedulers/                  # Tareas programadas
│   │   └── tareas.py
│   └── services/                    # Lógica de negocio
│       └── perfiles_service.py
├── requirements.txt
├── .gitignore
└── README.md
```

##  Instalación

### Prerrequisitos

- Python 3.9 o superior
- PostgreSQL (o cuenta de Supabase)
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/erickAlejandr0/APITourInPanama.git
   cd APITourInPanama
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv
   
   # En Linux/Mac
   source venv/bin/activate
   
   # En Windows
   venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear un archivo `.env` en la raíz del proyecto:
   ```env
   SUPABASE_DB_URL=postgresql://usuario:contraseña@host:puerto/database
   ```

5. **Ejecutar la aplicación**
   ```bash
   uvicorn app.main:app --reload
   ```

   La API estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

Una vez que la aplicación esté en ejecución, puedes acceder a:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints Principales

### Usuarios (`/user`)

- `POST /user/registrar` - Registrar nuevo usuario
- `POST /user/auth` - Autenticar usuario
- `GET /user/get/itinerario/{idUser}` - Obtener itinerario de usuario

### Actividades (`/actividad`)

- `GET /actividad/get` - Listar todas las actividades
- `GET /actividad/{idcategoria}` - Actividades por categoría
- `GET /actividad/cercanas_de/{lat}/{lon}/{radio}` - Buscar actividades cercanas
- `POST /actividad/comentarios/agregar` - Agregar comentario
- `POST /actividad/itinerario/agregar` - Agregar actividad al itinerario
- `DELETE /actividad/itinerario/eliminar/{idItinerario}` - Eliminar del itinerario

### Perfiles (`/perfil`)

- `GET /perfil/{idUser}` - Obtener perfil de usuario
- `POST /perfil/crear` - Crear perfil
- `PUT /perfil/actualizar` - Actualizar perfil

## Características Clave

### Búsqueda Geoespacial
Encuentra actividades turísticas cerca de tu ubicación utilizando coordenadas GPS y un radio de búsqueda personalizado.

```python
GET /actividad/cercanas_de/{lat}/{lon}/{radio}
```

### Sistema de Itinerarios
Los usuarios pueden guardar actividades en su itinerario personal para planificar sus visitas.

### Limpieza Automática
El scheduler elimina automáticamente las actividades expiradas del itinerario al iniciar la aplicación.

### CORS Configurado
La API acepta peticiones desde cualquier origen, facilitando la integración con aplicaciones frontend.

##  Base de Datos

El proyecto utiliza **Supabase** (PostgreSQL) con funciones almacenadas para operaciones complejas:

- `mostrar_actividades()`
- `actividades_por_categoria(idcategoria)`
- `registrar_usuario(...)`
- `autenticar_usuario(email, password)`
- `eliminar_actividades_expiradas()`

##  Seguridad

- Las contraseñas deben ser manejadas con hashing en la base de datos
- Las variables sensibles se gestionan mediante variables de entorno
- Validación de datos con Pydantic


## Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `SUPABASE_DB_URL` | URL de conexión a PostgreSQL/Supabase |  Sí |

## Manejo de Errores

La API retorna códigos de estado HTTP estándar:

- `200` - Éxito
- `400` - Error en la petición (ej. correo duplicado)
- `404` - Recurso no encontrado
- `500` - Error interno del servidor

##  Licencia

Este proyecto está bajo una licencia de código abierto.

##  Autores

- **Erick Alejandro** - [@erickAlejandr0](https://github.com/erickAlejandr0)


