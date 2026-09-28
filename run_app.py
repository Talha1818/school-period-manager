# run_app.py
#
# Entry point used when this project is packaged into a single .exe
# (see build_exe.py). Also runs fine directly with `python run_app.py`
# during development — it behaves the same as `manage.py runserver`,
# just with waitress as the server and the browser auto-opened.
#
# Data storage: the live database lives under
#   %LOCALAPPDATA%\PeriodManager\db.sqlite3
# — a per-Windows-user folder that always exists and is writable,
# regardless of where the .exe itself is installed (Program Files is
# read-only for normal users). Nothing is synced anywhere else.
import os
import sys
import shutil
import threading
import time
import webbrowser
from pathlib import Path

import django
from waitress import serve

# ---------------------------------------------------------------------
# Configure application
# ---------------------------------------------------------------------
BASE_DIR = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
from django.core.management import call_command

# ---------------------------------------------------------------------
# Database paths
# ---------------------------------------------------------------------
bundled_db = BASE_DIR / "db.sqlite3"          # seed data shipped inside the exe
target_db = Path(settings.DATABASES["default"]["NAME"])  # %LOCALAPPDATA%\PeriodManager\db.sqlite3

# App display name — derived from the .exe's own filename when frozen
# (so a renamed exe like SchoolTimetable.exe prints that name too),
# falls back to a dev-mode label otherwise.
APP_DISPLAY_NAME = Path(sys.executable).stem if getattr(sys, "frozen", False) else "Period Manager (dev)"

print("=" * 65)
print(f"                 {APP_DISPLAY_NAME} Starting...")
print("=" * 65)

# ---------------------------------------------------------------------
# First run — copy the seed database (with teachers/classes/periods/
# subjects already loaded) if the user doesn't have one yet.
# ---------------------------------------------------------------------
if not target_db.exists():
    if bundled_db.exists():
        shutil.copy(bundled_db, target_db)
        print("[INFO] Seed database copied to:")
        print(f"       {target_db}")
    else:
        print("[WARNING] Bundled database not found — starting empty.")
else:
    print(f"[INFO] Using existing database at:")
    print(f"       {target_db}")

# ---------------------------------------------------------------------
# Run migrations — every launch, no version gate.
# ---------------------------------------------------------------------
print("-" * 65)
print("[INFO] Checking database migrations...")
call_command("migrate", interactive=False, run_syncdb=True)
print("[INFO] Database is up to date.")
print("-" * 65)


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    from config.wsgi import application

    print("[INFO] Web Server          : RUNNING")
    print("[INFO] URL                 : http://127.0.0.1:8000")
    print("[INFO] Data folder         :", target_db.parent)
    print("[INFO] Press Ctrl+C to stop the application.")
    print("=" * 65)

    serve(
        application,
        host="127.0.0.1",
        port=8000,
    )
