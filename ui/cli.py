"""Interactive CLI for ResumeLens."""

import os
import sys
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from resumeLens.main import SAMPLES, process_resume, run_demo

MENU = """
ResumeLens
  1) Load a CV from a path
  2) Choose a sample CV
  3) Run all samples
  4) Open last report
  0) Exit
"""


def clean_path(raw: str) -> str:
    """Clean surrounding whitespace and quotes from raw path input."""
    return raw.strip().strip('"').strip("'")


def open_report(path: str) -> None:
    """Open the HTML report in the default system web browser."""
    webbrowser.open(Path(path).resolve().as_uri())


def load_cv(path: str) -> Optional[str]:
    """Run the pipeline on one file. Returns the html path or None."""
    try:
        result: Dict[str, Any] = process_resume(path)
    except FileNotFoundError as error:
        print(error)
        return None
    except Exception as error:
        print(f"Could not process the CV: {error}")
        return None

    name: str = result["extracted"].get("name", "Unknown")
    classification: Dict[str, Any] = result["classification"]
    print(f"\n{name}: {classification['profile']} -> {classification['result']}")

    html_path: str = result["paths"]["html"]
    if input("Open the report? [y/N] ").strip().lower() == "y":
        open_report(html_path)
    return html_path


def choose_sample() -> Optional[str]:
    """Display available sample resumes and run pipeline on selected sample."""
    available: List[str] = [s for s in SAMPLES if os.path.exists(s)]
    if not available:
        print("No sample CVs found.")
        return None

    for i, sample in enumerate(available, 1):
        print(f"  {i}) {os.path.basename(sample)}")
    choice: str = input("Sample number: ").strip()

    if not choice.isdigit() or not 1 <= int(choice) <= len(available):
        print("Invalid option.")
        return None
    return load_cv(available[int(choice) - 1])


def run() -> None:
    """Run the interactive CLI loop."""
    last_report: Optional[str] = None
    try:
        while True:
            print(MENU)
            option: str = input("> ").strip()

            if option == "1":
                path: str = clean_path(input("CV path: "))
                last_report = load_cv(path) or last_report
            elif option == "2":
                last_report = choose_sample() or last_report
            elif option == "3":
                run_demo()
            elif option == "4":
                if last_report:
                    open_report(last_report)
                else:
                    print("No report yet, load a CV first.")
            elif option == "0":
                break
            else:
                print("Invalid option.")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    run()