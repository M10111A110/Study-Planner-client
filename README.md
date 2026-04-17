# Smart Study Planner (CLI)

A simple command-line study planner to help you manage tasks and track your progress.

## Features
- Add study tasks with subject, topic, dates, and priority
- View all tasks with their status
- Mark tasks as complete
- Delete tasks

## Requirements
- Python 3.6+

## How to Run

```bash
cd src
python main.py
```

## Usage

On launch, you'll see a menu:

```
--- Study Planner ---
1. Add task
2. View tasks
3. Mark task complete
4. Delete task
5. Filter / Sort tasks
6. Edit task
7. Exit
```

Tasks are saved locally in `planner.json` inside the `src/` directory.

## Project Structure

```
Study-Planner-client/
├── src/
│   ├── main.py           # CLI entry point
│   ├── tasks_manager.py  # Task operations (add, view, complete, delete)
│   └── planner.json      # Local task storage (auto-created, not tracked by git)
├── CHANGELOG.md
└── README.md
```

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a full list of changes and bug fixes.