import subprocess
import os

def main():
    subprocess.Popen([os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dist', 'meditor-1.0.0.exe')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)