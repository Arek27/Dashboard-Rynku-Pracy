import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APP = ROOT / "app.py"
REQ = ROOT / "requirements.txt"

def run(cmd):
    subprocess.run(cmd, check=True)

def main():
    if not APP.exists():
        raise FileNotFoundError("Nie znaleziono app.py")

    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    if REQ.exists():
        run([sys.executable, "-m", "pip", "install", "-r", str(REQ)])

    run([sys.executable, "-m", "streamlit", "run", str(APP)])

if __name__ == "__main__":
    main()

