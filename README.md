Smart Task Manager

Smart Task Manager is a personal productivity web app that helps authenticated users create, manage, and complete tasks quickly. It combines a clean Django back end (with models, forms, and authenticated views) and a progressive, mobile‑first front end enhanced by JavaScript for live interactions such as instant search/filtering and asynchronous status toggling.

Distinctiveness and Complexity

This project is not a social network or an e‑commerce site and is more complex than prior CS50W projects in several ways:

1) Feature depth beyond CRUD: In addition to create/read/update/delete, the dashboard supports multi‑criteria sorting, server‑side filtering, and client‑side live search and status filtering with no page reloads. It also implements an AJAX endpoint to toggle task completion asynchronously, updating the DOM and preserving CSRF security.

2) Full‑stack interactivity: The app uses Django for models, authentication, server‑side validation, and messaging, while the front end adds JavaScript behaviors (debounced search/filter, async toggle) and a responsive layout. This explicit separation of responsibilities goes beyond the static forms typical of earlier projects.

3) Mobile‑responsive UX: The layout uses responsive grids, touch‑friendly controls, and a sticky navigation, ensuring an optimal experience across phones, tablets, and desktops.

4) Clean architecture and extensibility: The codebase follows Django best practices with an app (`tasks`) containing `models`, `forms`, `views`, `urls`, templates, and static assets. The AJAX pattern used for toggle can be extended to inline edit, bulk actions, and real‑time updates.

Together, these choices make the project distinct and meaningfully more complex, while remaining focused on task management rather than replicating prior course assignments.

Project Structure

smarttask/ (project config)
 ├─ settings.py — Django settings, installed apps, auth redirects, static config
 ├─ urls.py — root URL routing, includes `tasks` and built‑in auth URLs

tasks/ (application)
 ├─ models.py — `Task` model with priority, due date, completion, and user FK
 ├─ forms.py — `TaskForm` for create/edit
 ├─ views.py — dashboard, create/edit/delete, register, and AJAX endpoints
 ├─ urls.py — named routes for UI and API (`toggle_task_api`)
 ├─ static/tasks/app.js — front‑end JS for live search/filter and async toggle
 └─ templates/tasks/
    ├─ base.html — responsive shell, nav, messages, and JS include
    ├─ dashboard.html — search/sort/filter UI and task list
    ├─ task_create.html — create form
    ├─ task_edit.html — edit form
    └─ task_confirm_delete.html — delete confirmation

How to Run

1) Create and activate a virtual environment (recommended)
   - Windows (PowerShell):
     - python -m venv env
     - .\env\Scripts\Activate.ps1

2) Install dependencies:
   - pip install -r requirements.txt

3) Apply migrations and run the server:
   - python manage.py migrate
   - python manage.py runserver

4) Visit the app at `http://127.0.0.1:8000/`. Use Register to create an account, then create tasks from the Dashboard.

Feature Highlights

- Authentication: Register, Login, Logout (Django auth)
- Tasks: Create, Edit, Delete, Toggle Complete
- Sorting: Due date, priority, title, status
- Filtering: Server‑side by status; client‑side live query and status filter
- Async toggle: Toggle completion without page reload via `fetch` + CSRF
- Responsive UI: Grid controls, sticky nav, touch targets, semantic defaults

Additional Notes

- Security: CSRF protection is preserved for AJAX calls and all modifying endpoints require authentication.
- Extensibility: The AJAX pattern can be reused for inline edits, batch operations, or adding tags/reminders.
- Database: SQLite by default; switching to Postgres requires updating `DATABASES` in `settings.py`.

Requirements

See `requirements.txt` for pinned versions. Core dependency:

- Django==4.2.23
