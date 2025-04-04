import unittest
from Python_Projects.Task_Manager.tasks import add_task, list_tasks, complete_task, delete_task
from Python_Projects.Task_Manager.database import get_db_connection, initialize_db  # Importa funciones relacionadas con la base de datos

class TestTaskManager(unittest.TestCase):
    """
    Clase de pruebas para el gestor de tareas.
    Contiene métodos para probar las funcionalidades principales.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Configura la base de datos de prueba antes de ejecutar las pruebas.
        Este método se ejecuta una vez antes de todas las pruebas.
        """
        initialize_db()  # Inicializa la base de datos para pruebas

    def test_add_task(self):
        """
        Prueba la funcionalidad de agregar una tarea.
        Verifica que la tarea se haya agregado correctamente a la base de datos.
        """
        add_task("Test Task")  # Agrega una tarea de prueba
        conn = get_db_connection()  # Obtiene la conexión a la base de datos
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE title = 'Test Task'")  # Busca la tarea agregada
        task = cursor.fetchone()  # Obtiene el resultado
        conn.close()  # Cierra la conexión
        self.assertIsNotNone(task)  # Verifica que la tarea exista en la base de datos

# Punto de entrada principal para ejecutar las pruebas
if __name__ == "__main__":
    unittest.main()  # Ejecuta las pruebas
