"""Run the current project checker; earlier versions remain in project-check/."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "project-check/v002/check_project.py"), run_name="__main__")
