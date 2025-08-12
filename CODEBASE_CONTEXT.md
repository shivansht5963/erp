# Codebase Context Summary

This file provides an overview of the main directories and files in your Django ERP project.

## Main Directories & Files

- `accounts/`
  - admin.py, apps.py, forms.py, migrations/, models.py, tests.py, urls.py, views.py, __init__.py
- `attendance/`
  - admin.py, apps.py, migrations/, models.py, tests.py, urls.py, views.py, __init__.py
- `erp/` (project settings)
  - asgi.py, settings.py, urls.py, views.py, wsgi.py, __init__.py
- `exams/`
  - admin.py, apps.py, migrations/, models.py, tests.py, urls.py, views.py, __init__.py
- `faculty/`
  - admin.py, apps.py, forms.py, migrations/, models.py, tests.py, urls.py, views.py, __init__.py
- `fees/`
  - admin.py, apps.py, migrations/, models.py, tests.py, urls.py, views.py, __init__.py
- `students/`
  - admin.py, apps.py, forms.py, migrations/, models.py, tests.py, urls.py, views.py, __init__.py
- `static/` (static files)
- `templates/` (HTML templates)
- `db.sqlite3` (SQLite database)
- `manage.py` (Django management script)
- `README.md` (project instructions)
- `requirements.txt` (Python dependencies)
- `recruitment.txt` (recruitment module template)
- `erp_custom_diagram.png`, `erp_diagram.png` (project diagrams)

---
Each app contains its own models, views, admin, migrations, and other Django files. The `erp/` directory holds the main project settings and configuration.
