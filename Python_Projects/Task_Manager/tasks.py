from database import get_db_connection  # Importa la función para conectarse a la base de datos

def add_task(title, due_date=None, priority="Medium", category="General"):
    """
    Agrega una nueva tarea a la base de datos.
    Parámetros:
      - title: Título de la tarea.
    """
    conn = get_db_connection()  # Obtiene la conexión a la base de datos
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, due_date, priority, category) 
        VALUES (?, ?, ?, ?)
    """, (title, due_date, priority, category)) # Inserta la nueva tarea
    conn.commit()  # Confirma los cambios
    conn.close()  # Cierra la conexión
    print(f"Task '{title}' added successfully with priority {priority} and due date {due_date}.") # Mensaje de confirmación

from datetime import datetime
from plyer import notification

def list_tasks(filter_by=None, sort=None):
    """
    Recupera y muestra todas las tareas almacenadas en la base de datos con opciones de filtro y orden.
    Parámetros:
      - filter_by: Diccionario con claves como 'category', 'priority', 'completed' para filtrar las tareas.
      - order_by: Campo por el cual ordenar las tareas (por ejemplo, 'due_date', 'priority').
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []


    # Agrega filtros si se proporcionan
    if filter_by:
        filter_by_lower = filter_by.lower()
        if filter_by_lower == "completed":
            query += " AND completed = 1"
        elif filter_by_lower == "pending":
            query += " AND completed = 0"
        elif filter_by_lower in ["high", "medium", "low"]:
            query += " AND priority = ?"
            params.append(filter_by.capitalize())
        else:
            query += " AND category = ?"
            params.append(filter_by)

    # **📌 Apply Sorting**
    if sort == "due":
        query += " ORDER BY due_date ASC"
    elif sort == "priority":
        query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END"

    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:  # Verifica si no hay tareas
        print("No tasks found.")  # Mensaje si no hay tareas
        return

    # Muestra la lista de tareas con su estado
    print("\n📋 Task List:")

    today = datetime.today().date()
    for task in tasks:
        status = "✔️ Completed" if task["completed"] else "❌ Pending"
        due_date = task["due_date"]

        if due_date:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
            days_remaining = (due_date_obj - today).days

            # **📌 ALERTAS DE VENCIMIENTO**
            if days_remaining == 0:
                alert_message = f"⚠️ Task '{task['title']}' is due TODAY!"
                print(alert_message)
                notification.notify(
                    title="Task Due Today!",
                    message=alert_message,
                    timeout=5
                )

            elif days_remaining < 0:
                alert_message = f"❌ Task '{task['title']}' was due on {due_date}!"
                print(alert_message)
                notification.notify(
                    title="Overdue Task!",
                    message=alert_message,
                    timeout=5
                )

            elif days_remaining <= 3:
                alert_message = f"⚠️ Task '{task['title']}' is due in {days_remaining} days."
                print(alert_message)
                notification.notify(
                    title="Upcoming Task Reminder",
                    message=alert_message,
                    timeout=5
                )

            due_display = f"(Due: {due_date})"
        else:
            due_display = "(No Due Date)"

        print(f"{task['id']}. [{task['priority']}] {task['title']} - {task['category']} {due_display} - {status}")

def complete_task(task_id):
    """
    Marca una tarea como completada.
    Parámetros:
      - task_id: ID de la tarea a completar.
    """
    conn = get_db_connection()  # Obtiene la conexión a la base de datos
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))  # Actualiza el estado de la tarea
    conn.commit()  # Confirma los cambios
    conn.close()  # Cierra la conexión
    print(f"Task {task_id} marked as completed.")  # Mensaje de confirmación

def delete_task(task_id):
    """
    Elimina una tarea de la base de datos.
    Parámetros:
      - task_id: ID de la tarea a eliminar.
    """
    conn = get_db_connection()  # Obtiene la conexión a la base de datos
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))  # Elimina la tarea por ID
    conn.commit()  # Confirma los cambios
    conn.close()  # Cierra la conexión
    print(f"Task {task_id} deleted successfully.")  # Mensaje de confirmación

from datetime import datetime

def list_overdue_tasks():
    """
    Lista las tareas que están vencidas (overdue).
    Una tarea se considera vencida si su fecha de vencimiento (due_date) es anterior a la fecha actual
    y no ha sido marcada como completada.
    """
    # Obtiene la fecha actual en formato 'YYYY-MM-DD'
    today = datetime.today().strftime('%Y-%m-%d')
    
    # Establece una conexión con la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Consulta las tareas que tienen una fecha de vencimiento anterior a hoy y no están completadas
    cursor.execute("SELECT * FROM tasks WHERE due_date < ? AND completed = 0", (today,))
    tasks = cursor.fetchall()  # Obtiene todas las tareas que cumplen con la condición
    conn.close()  # Cierra la conexión a la base de datos

    # Si no hay tareas vencidas, muestra un mensaje y termina la función
    if not tasks:
        print("No overdue tasks.")
        return

    # Muestra las tareas vencidas con su información
    print("\n⏳ Overdue Tasks:")
    for task in tasks:
        # Imprime el ID, prioridad, título, categoría y fecha de vencimiento de cada tarea
        print(f"{task['id']}. [{task['priority']}] {task['title']} - {task['category']} (Due: {task['due_date']}) ❌ Overdue")

    