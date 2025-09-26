from flask import Flask, request, jsonify
import mysql.connector
import config
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Decorador para rutas protegidas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Conexión a DB
def get_db():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

# Registro
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'])
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return jsonify({'message': 'User created successfully'})
    except mysql.connector.Error as err:
        return jsonify({'message': str(err)})
    finally:
        cursor.close()
        db.close()

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = jwt.encode({'user_id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

# Crear tarea
@app.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    title = data['title']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (user_id, title) VALUES (%s, %s)", (current_user, title))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Task created'})

# Listar tareas
@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, title, completed FROM tasks WHERE user_id=%s", (current_user,))
    tasks = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(tasks)

# Marcar tarea como completada
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def complete_task(current_user, task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET completed=TRUE WHERE id=%s AND user_id=%s", (task_id, current_user))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Task marked as completed'})

# Eliminar tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s AND user_id=%s", (task_id, current_user))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)
