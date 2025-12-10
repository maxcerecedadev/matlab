import os
import shutil
import subprocess
import sys

VENV_DIR = "venv"

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # 1) Borrar venv si existe
    if os.path.isdir(VENV_DIR):
        print(f"Eliminando entorno virtual existente: {VENV_DIR}")
        shutil.rmtree(VENV_DIR)

    # 2) Crear nuevo venv
    print("Creando nuevo entorno virtual...")
    subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

    # Ruta al python del venv (Windows)
    if os.name == "nt":
        venv_python = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(VENV_DIR, "bin", "python")

    # 3) Instalar requirements
    requirements_path = os.path.join(project_root, "requirements.txt")
    if not os.path.isfile(requirements_path):
        raise FileNotFoundError("No se encontró requirements.txt en la raíz del proyecto")

    print("Instalando dependencias desde requirements.txt...")
    subprocess.check_call([venv_python, "-m", "pip", "install", "-r", requirements_path])

    # 4) Ejecutar servidor Django
    manage_py = os.path.join(project_root, "manage.py")
    if not os.path.isfile(manage_py):
        raise FileNotFoundError("No se encontró manage.py en la raíz del proyecto")

    print("Levantando servidor: python manage.py runserver")
    subprocess.check_call([venv_python, "manage.py", "runserver"])

if __name__ == "__main__":
    main()
