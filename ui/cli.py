import sys
import os
import webbrowser
from pathlib import Path


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


def clean_path(raw):
    # dragging a file into the terminal on windows adds quotes
    return raw.strip().strip('"').strip("'")


def open_report(path):
    webbrowser.open(Path(path).resolve().as_uri())


def load_cv(path):
    #run the pipeline on one file. returns the html path or none
    try:
        result = process_resume(path)
    except FileNotFoundError as error:
        print(error)
        return None
    except Exception as error:
        print(f"Could not process the CV: {error}")
        return None

    name = result["extracted"].get("name", "Unknown")
    classification = result["classification"]
    print(f"\n{name}: {classification['profile']} -> {classification['result']}")

    html_path = result["paths"]["html"]
    if input("Open the report? [y/N] ").strip().lower() == "y":
        open_report(html_path)
    return html_path


def choose_sample():
    available = [s for s in SAMPLES if os.path.exists(s)]
    if not available:
        print("No sample CVs found.")
        return None

    for i, sample in enumerate(available, 1):
        print(f"  {i}) {os.path.basename(sample)}")
    choice = input("Sample number: ").strip()

    if not choice.isdigit() or not 1 <= int(choice) <= len(available):
        print("Invalid option.")
        return None
    return load_cv(available[int(choice) - 1])


def run():
    last_report = None
    try:
        while True:
            print(MENU)
            option = input("> ").strip()

            if option == "1":
                path = clean_path(input("CV path: "))
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