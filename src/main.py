from tasks_manager import *

# Load existing tasks from planner.json at startup (or initialize an empty list)
data = load_tasks()

while True:
    print("\n--- Study Planner ---")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task complete")
    print("4. Delete task")
    print("5. Filter / Sort tasks")
    print("6. Edit task")
    print("7. Exit")

    choice = int(input("Choose an option:\t"))

    if choice == 1:
        add_task(data)
    elif choice == 2:
        view_task(data)
    elif choice == 3:
        mark_complete(data)
    elif choice == 4:
        del_task(data)
    elif choice == 5:
        filter_sort_tasks(data)
    elif choice == 6:
        edit_task(data)
    elif choice == 7:
        break
    else:
        print("Invalid option, try again")