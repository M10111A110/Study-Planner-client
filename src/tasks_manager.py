import json
import os

# Path to the local JSON file used as task storage
FILE = "planner.json"


def load_tasks():
    """Load tasks from the JSON file. Returns an empty task list if the file doesn't exist."""
    if not os.path.exists(FILE):
        return {"tasks": []}
    with open(FILE, 'r') as file:
        return json.load(file)


def save_tasks(data):
    """Persist the current task data to the JSON file."""
    with open(FILE, 'w') as file:
        json.dump(data, file, indent=2)


def add_task(data):
    """Prompt the user for task details and append a new task to the task list."""
    sub = input("Subject:\t")
    topic = input("Topic:\t")
    assign = input("Assigning Date (DD-MM-YYYY):\t")
    due = input("Due Date (DD-MM-YYYY):\t")
    priority = int(input("Priority (1-10):\t"))

    # Auto-increment ID based on the current maximum; defaults to 0 if no tasks exist
    task = {
        "id": max((task["id"] for task in data["tasks"]), default=0) + 1,
        "subject": sub,
        "topic": topic,
        "assign_date": assign,
        "due_date": due,
        "priority": priority,
        "status": "Pending",   # New tasks always start as Pending
        "complete_date": ""    # Empty until the task is marked complete
    }

    data["tasks"].append(task)
    save_tasks(data)
    print("Task has been added\n")


def view_task(data, tasks=None):
    """
    Display tasks in a readable format.
    If a filtered/sorted list is passed via `tasks`, that list is shown;
    otherwise all tasks in `data` are displayed.
    """
    # Use the provided subset of tasks, or fall back to the full list
    tasks = tasks if tasks is not None else data["tasks"]

    if not data["tasks"]:
        print("No tasks added yet")
        return

    for task in tasks:
        print(f"\n[{task['id']}] {task['subject']} - {task['topic']}")
        print(f"Due: {task['due_date']} | Priority: {task['priority']} | Status: {task['status']}")


def mark_complete(data):
    """Display all tasks, then mark a user-selected task as Completed and record the completion date."""
    view_task(data)
    task_id = int(input("\nEnter task ID to mark its completion:\t"))

    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = "Completed"
            inp = input("Date of Completion (DD-MM-YYYY):\t")
            task["complete_date"] = inp
            save_tasks(data)
            print(str(task_id) + " Marked Complete")
            return

    print("Task not found")


def del_task(data):
    """Display all tasks, then permanently remove the task with the given ID."""
    view_task(data)
    task_id = int(input("\nEnter task ID to delete:\t"))

    # Rebuild the list excluding the deleted task
    data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
    save_tasks(data)
    print(str(task_id) + " Task deleted")


def edit_task(data):
    """
    Display all tasks, then allow the user to edit any fields of a selected task.
    Pressing Enter without input keeps the existing value for that field.
    """
    if not data["tasks"]:
        print("No tasks found")
        return

    view_task(data)
    task_id = int(input("\nEnter task ID to edit:\t"))

    # Find the task by ID; returns None if not found
    task = next((t for t in data["tasks"] if t["id"] == task_id), None)
    if not task:
        print("Task not found")
        return

    print(f"\nEditing Task [{task_id}] — leave blank to keep current value")

    # Collect new values; blank input means "no change"
    new_sub = input(f"Subject [{task['subject']}]:\t").strip()
    new_topic = input(f"Topic [{task['topic']}]:\t").strip()
    new_assign = input(f"Assigning Date [{task['assign_date']}]:\t").strip()
    new_due = input(f"Due Date [{task['due_date']}]:\t").strip()
    new_priority = input(f"Priority [{task['priority']}] (1-10):\t").strip()

    # Only update fields where the user provided a new value
    if new_sub:
        task["subject"] = new_sub
    if new_topic:
        task["topic"] = new_topic
    if new_assign:
        task["assign_date"] = new_assign
    if new_due:
        task["due_date"] = new_due
    if new_priority:
        task["priority"] = int(new_priority)

    save_tasks(data)
    print(f"Task {task_id} updated successfully")


def filter_sort_tasks(data):
    """
    Let the user filter tasks by status (All / Pending / Completed)
    and optionally sort them by priority or due date before displaying.
    """
    if not data["tasks"]:
        print("No tasks found")
        return

    # --- Filter step ---
    print("\n-- Filter --")
    print("1. All tasks")
    print("2. Pending only")
    print("3. Completed only")
    filter_choice = input("Choose filter:\t").strip()

    if filter_choice == "2":
        filtered = [t for t in data["tasks"] if t["status"] == "Pending"]
    elif filter_choice == "3":
        filtered = [t for t in data["tasks"] if t["status"] == "Completed"]
    else:
        # Default: include all tasks
        filtered = list(data["tasks"])

    # --- Sort step ---
    print("\n-- Sort --")
    print("1. No sorting")
    print("2. Sort by priority (high to low)")
    print("3. Sort by due date (earliest first)")
    sort_choice = input("Choose sort:\t").strip()

    if sort_choice == "2":
        # Higher priority number = more urgent; sort descending
        filtered.sort(key=lambda t: t["priority"], reverse=True)
    elif sort_choice == "3":
        def parse_date(date):
            """Convert DD-MM-YYYY string to a (year, month, day) tuple for correct chronological sorting."""
            try:
                day, month, year = date.split("-")
                return (int(year), int(month), int(day))
            except ValueError:
                # Push malformed dates to the end of the sorted list
                return (9999, 99, 99)

        filtered.sort(key=lambda t: parse_date(t["due_date"]))

    if not filtered:
        print("No tasks match the selected filter")
    else:
        view_task(data, tasks=filtered)