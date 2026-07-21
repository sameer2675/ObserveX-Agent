import subprocess
import os
import sys
from storage.register import already_registered


def resource_path(filename):
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(__file__), filename)


def launch(py_file, exe_file):
    if getattr(sys, "frozen", False):
        subprocess.Popen([resource_path(exe_file)])
    else:
        subprocess.Popen([sys.executable, resource_path(py_file)])


def main():
    if already_registered():
        print("Already registered - service handles the agent, nothing to launch")
    else:
        print("Not Registered")
        launch("registration.py", "registration.exe")
if __name__ == "__main__":
    main()