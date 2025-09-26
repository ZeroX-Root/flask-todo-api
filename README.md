# To-Do List Flask API

Una API RESTful para gestionar tareas (to-do list) con autenticación JWT, desarrollada con Flask y MySQL.

## Características
- Registro y login de usuarios con contraseña hasheada
- Autenticación y autorización con JWT
- CRUD de tareas por usuario
- Base de datos relacional MySQL

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/ZeroX-Root/flask-todo-api.git
   cd to-do-list-flask
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la base de datos:**
   - Asegúrate de tener MySQL corriendo.
   - Ejecuta el script `database.sql` para crear la base de datos y tablas:
     ```bash
     mysql -u <usuario> -p < database.sql
     ```
   - Modifica `config.py` si es necesario para tus credenciales.

4. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

## Endpoints principales

- `POST   /register`   → Registro de usuario
- `POST   /login`      → Login y obtención de token JWT
- `POST   /tasks`      → Crear tarea (requiere JWT)
- `GET    /tasks`      → Listar tareas del usuario (requiere JWT)
- `PUT    /tasks/<id>` → Marcar tarea como completada (requiere JWT)
- `DELETE /tasks/<id>` → Eliminar tarea (requiere JWT)

El token JWT debe enviarse en el header `x-access-token`.


## Uso de token JWT desde archivo `.env`

Puedes guardar tu token JWT en un archivo `.env` para facilitar el uso de los comandos curl. Ejemplo de `.env`:

```env
TOKEN=tu_token_jwt_aqui
```

Luego, en tu terminal, carga el token con:

```bash
export $(grep TOKEN .env)
```

Y usa los siguientes comandos:

```bash
# Registro
curl -X POST -H "Content-Type: application/json" -d '{"username":"usuario","password":"clave"}' http://localhost:5000/register

# Login (guarda el token manualmente en .env)
curl -X POST -H "Content-Type: application/json" -d '{"username":"usuario","password":"clave"}' http://localhost:5000/login
# Copia el valor del token de la respuesta y pégalo en tu archivo .env

# Crear tarea
curl -X POST -H "Content-Type: application/json" -H "x-access-token: $TOKEN" -d '{"title":"Mi tarea"}' http://localhost:5000/tasks

# Listar tareas
curl -X GET -H "x-access-token: $TOKEN" http://localhost:5000/tasks
```



---

⚠️ **Importante:**

- Si cierras la terminal y abres otra, deberás ejecutar `source .env` de nuevo para cargar las variables.
- Si el token que tienes en `.env` ya expiró, aunque hagas `source .env`, seguirás recibiendo "Token is invalid!". En ese caso, hay que generar un token nuevo haciendo login y actualizar el `.env`.

---

## Estructura del proyecto

```
app.py           # Código principal de la API
config.py        # Configuración de la base de datos y clave secreta
requirements.txt # Dependencias
README.md        # Este archivo
__pycache__/     # Archivos temporales de Python
database.sql     # Script para crear la base de datos y tablas
```
