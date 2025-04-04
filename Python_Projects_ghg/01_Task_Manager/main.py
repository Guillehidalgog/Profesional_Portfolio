import argparse
from tasks import add_task, list_tasks, complete_task, delete_task, list_overdue_tasks

def main():
    # Configura el analizador de argumentos para la CLI
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")  # Define subcomandos para diferentes acciones

    # Subcomando para agregar una nueva tarea
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("title", type=str, help="Task title")
    parser_add.add_argument("--due", type=str, help="Due date (YYYY-MM-DD)", default=None)
    parser_add.add_argument("--priority", type=str, choices=["Low", "Medium", "High"], default="Medium", help="Task priority")
    parser_add.add_argument("--category", type=str, help="Task category", default="General")

    # Subcomando para listar todas las tareas con filtros y orden
    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.add_argument("--filter", type=str, help="Filter by priority, category, or 'completed'")
    parser_list.add_argument("--sort", type=str, choices=["due", "priority"], help="Sort tasks by due date or priority")

    # Subcomando para listar tareas vencidas
    subparsers.add_parser("overdue", help="List overdue tasks")

    # Subcomando para marcar una tarea como completada
    parser_complete = subparsers.add_parser("complete", help="Mark a task as completed")
    parser_complete.add_argument("task_id", type=int, help="Task ID to complete")

    # Subcomando para eliminar una tarea
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("task_id", type=int, help="Task ID to delete")

    # Analiza los argumentos proporcionados por el usuario
    args = parser.parse_args()

    # Ejecuta la acción correspondiente según el subcomando
    if args.command == "add":
        add_task(args.title, args.due, args.priority, args.category)
    elif args.command == "list":
        list_tasks(filter_by=args.filter, sort=args.sort)
    elif args.command == "complete":
        complete_task(args.task_id)
    elif args.command == "delete":
        delete_task(args.task_id)
    else:
        parser.print_help() # Muestra la ayuda si no se proporciona un subcomando válido

# Punto de entrada principal del script
if __name__ == "__main__":
    main()  # Llama a la función principal
