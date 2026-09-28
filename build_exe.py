# build_exe.py
#
# Builds Period Manager into a single-folder Windows .exe using
# PyInstaller. Run this on Windows (PyInstaller builds are not
# cross-platform):
#
#     pip install -r requirements.txt
#     pip install pyinstaller
#     python build_exe.py
#
# Output goes to dist\PeriodManager\ — that whole folder is the app
# (PeriodManager.exe plus everything it needs). Feed that folder to
# installer.iss (Inno Setup) to build a proper installer, or just zip
# it and hand it over as-is; PeriodManager.exe works standalone too.
import os
import shutil
import subprocess
import sys
from pathlib import Path

import PyInstaller.__main__

BASE_DIR = Path(__file__).resolve().parent
APP_NAME = "PeriodManager"
SEP = ";" if os.name == "nt" else ":"  # PyInstaller --add-data separator


def add_data(src: str, dest: str) -> str:
    return f"{BASE_DIR / src}{SEP}{dest}"


def main():
    # Clear previous build output so stale files never sneak into a new build.
    for folder in ("build", "dist"):
        shutil.rmtree(BASE_DIR / folder, ignore_errors=True)

    # The exe ships db.sqlite3 as its seed data (teachers/classes/periods/
    # subjects pre-loaded) — build it fresh if it isn't there yet.
    db_path = BASE_DIR / "db.sqlite3"
    if not db_path.exists():
        print("[INFO] No db.sqlite3 found — running migrations to create the seed database...")
        subprocess.run([sys.executable, "manage.py", "migrate"], cwd=BASE_DIR, check=True)

    args = [
        "run_app.py",
        f"--name={APP_NAME}",
        "--onedir",
        "--noconfirm",
        "--console",  # keep the console window — shows startup/status messages
        # Ship a ready-made database (teachers/classes/periods/subjects
        # already loaded) as the seed copied to %LOCALAPPDATA% on first run.
        "--add-data", add_data("db.sqlite3", "."),
        "--add-data", add_data("templates", "templates"),
        "--add-data", add_data("static", "static"),
        # Django apps are imported dynamically (via INSTALLED_APPS / migrations),
        # so PyInstaller can't see those imports by static analysis — list them
        # explicitly instead.
        "--hidden-import", "whitenoise.middleware",
        "--hidden-import", "whitenoise.runserver_nostatic",
        "--collect-submodules", "django.contrib.admin",
        "--collect-submodules", "django.contrib.auth",
        "--collect-submodules", "django.contrib.sessions",
        "--collect-submodules", "django.contrib.messages",
        "--collect-submodules", "django.contrib.staticfiles",
        "--collect-submodules", "timetable",
        "--collect-submodules", "timetable.migrations",
        "--collect-submodules", "config",
    ]

    # Optional: use logo.ico as the .exe's icon, if present.
    icon = BASE_DIR / "logo.ico"
    if icon.exists():
        args.append(f"--icon={icon}")

    PyInstaller.__main__.run(args)

    print("\nBuild finished.")
    print(f"App folder: {BASE_DIR / 'dist' / APP_NAME}")
    print(f"Run it directly with: dist\\{APP_NAME}\\{APP_NAME}.exe")
    print("Or build an installer from it with installer.iss (Inno Setup).")


if __name__ == "__main__":
    sys.exit(main())
