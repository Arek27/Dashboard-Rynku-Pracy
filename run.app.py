import subprocess
import sys
from pathlib import Path

APP_FILE = Path(__file__).parent / "app.py"

def main():
    if not APP_FILE.exists():
        raise FileNotFoundError("Nie znaleziono pliku app.py")

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(APP_FILE)],
        check=True,
    )

if __name__ == "__main__":
    main()
