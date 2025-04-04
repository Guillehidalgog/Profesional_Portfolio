import sqlite3

# Nombre del archivo de la base de datos SQLite
DB_NAME = "Python_Projects/Task_Manager/tasks.db"

def get_db_connection():
    """
    Establece y devuelve una conexión a la base de datos SQLite.
    Configura la conexión para que las filas puedan ser accedidas como diccionarios.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

def initialize_db():
    """
    Crea la tabla 'tasks' en la base de datos si no existe.
    La tabla incluye:
      - id: Clave primaria autoincremental.
      - title: Título de la tarea (obligatorio).
      - completed: Estado de la tarea (booleano, por defecto False).
    """
    conn = get_db_connection()  # Obtiene la conexión a la base de datos
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT,  -- Stores task deadline
            priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')),  -- Task priority
            category TEXT,  -- Task category
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)  # Crea la tabla si no existe
    conn.commit()  # Confirma los cambios
    conn.close()  # Cierra la conexión

# Punto de entrada principal del script
if __name__ == "__main__":
    initialize_db()  # Inicializa la base de datos
    print("Database initialized successfully.")  # Mensaje de confirmación
