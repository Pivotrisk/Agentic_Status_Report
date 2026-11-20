"""Run the shared archive command from this portfolio's scripts folder."""
import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[3] / "archive_case.py"), run_name="__main__")
