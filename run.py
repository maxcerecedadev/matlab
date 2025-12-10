import os
import sys
import subprocess

VENV_DIR = "venv"


def get_venv_python(venv_dir: str) -> str:
    if os.name == "nt":
        # Windows
        return os.path.join(venv_dir, "Scripts", "python.exe")
    # Linux / macOS
    return os.path.join(venv_dir, "bin", "python")


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    manage_py = os.path.join(project_root, "manage.py")
    if not os.path.isfile(manage_py):
        print("No se encontró manage.py en la raíz del proyecto.")
        sys.exit(1)

    venv_python = get_venv_python(VENV_DIR)
    if not os.path.isfile(venv_python):
        print(f"No se encontró el intérprete de Python del venv en: {venv_python}")
        print("Asegúrate de haber creado el venv primero.")
        sys.exit(1)

    # Puedes cambiar el puerto aquí si quieres, por defecto 8000
    runserver_addr = "127.0.0.1:8000"

    print(f"Usando intérprete: {venv_python}")
    print(f"Levantando servidor Django en {runserver_addr}...")
    subprocess.check_call([venv_python, "manage.py", "runserver", runserver_addr])


if __name__ == "__main__":
    main()
