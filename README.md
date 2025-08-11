# ERP Django Template

This is a beginner-friendly ERP system template built with Django. Follow these steps to set up and run the project locally.

## Prerequisites
- Python 3.10+
- pip (Python package manager)
- Git (optional, for cloning)

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd erp_shiva/erp
   ```

2. **Create a virtual environment (recommended)**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure
- `accounts/`, `attendance/`, `exams/`, `faculty/`, `fees/`, `students/`: Django apps for different modules
- `erp/`: Main project settings
- `static/`: Static files (CSS, JS, images)
- `templates/`: HTML templates

## Notes
- The database file `db.sqlite3` is not included. It will be created automatically.
- Add your environment variables in a `.env` file if needed.
- For production, update `ALLOWED_HOSTS` in `erp/settings.py`.

## Troubleshooting
- If you get errors, check that all dependencies are installed and migrations are applied.
- For help, see the [Django documentation](https://docs.djangoproject.com/en/4.0/).

---
Feel free to customize this template for your needs!
