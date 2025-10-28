# -----------------------------------------------
# File: main.py
# Purpose: Entry point for Automata-based Code Analysis
# -----------------------------------------------

from automata.finite_automata import FiniteAutomata
from automata.pattern_definitions import PATTERN_LIST
from analyzer.code_scanner import tokenize_code, read_code_file
from utils.report_generator import generate_report
import os

def analyze_file(file_path):
    code = read_code_file(file_path)
    tokens = tokenize_code(code)

    results = []
    for vuln_name, details in PATTERN_LIST.items():
        fa = FiniteAutomata(
            states=details['states'],
            start_state=details['start'],
            accept_states=details['accept'],
            transitions=details['transitions']
        )

        if fa.process_input(tokens):
            results.append(f"⚠️  Vulnerability Detected: {vuln_name} in {os.path.basename(file_path)}")
        else:
            results.append(f"✅  No {vuln_name} in {os.path.basename(file_path)}")

    return results


if __name__ == "__main__":
    folder_path = "data/samples"
    all_results = []

    for file in os.listdir(folder_path):
        if file.endswith(".py"):
            path = os.path.join(folder_path, file)
            print(f"\n🔍 Scanning {file} ...")
            file_results = analyze_file(path)
            for r in file_results:
                print(r)
                all_results.append(r)

    generate_report(all_results)
# main.py
from analyzer.ast_detector import analyze_file
import os
from utils.report_generator import generate_report

if __name__ == "__main__":
    folder_path = "data/samples"
    all_results = []

    for file in os.listdir(folder_path):
        if file.endswith(".py"):
            path = os.path.join(folder_path, file)
            print(f"\n🔍 Scanning {file} ...")
            file_results = analyze_file(path)
            for r in file_results:
                print(r)
                all_results.append(r)

    generate_report(all_results)

# --- Auto-generate automata diagrams for demo/paper ---
try:
    from visualizer.automata_visualizer import draw_pattern
    from automata.pattern_definitions import PATTERN_LIST_FOR_VIS

    print("\n🎨 Generating automata diagrams...")
    for name, defn in PATTERN_LIST_FOR_VIS.items():
        # transitions expected as list of (from, symbol, to)
        draw_pattern(name, defn['states'], defn['transitions'], defn['start'], defn['accept'], output_dir='results')
    print("🎨 Done. Diagrams saved to results/ directory.")
except Exception as e:
    print("⚠️ Could not generate diagrams:", e)


from visualizer.automata_visualizer import draw_pattern
from automata.pattern_definitions import PATTERN_LIST_FOR_VIS  # create below

# Example small pattern definition suitable for visualization:
PATTERN_LIST_FOR_VIS = {
    "SQL Injection": {
        'states': ['start','input_received','concat','vulnerable'],
        'start': 'start',
        'accept': ['vulnerable'],
        'transitions': [
            ('start','input','input_received'),
            ('input_received','+','concat'),
            ('concat','SQL','vulnerable')
        ]
    }
}

# draw all
for name, defn in PATTERN_LIST_FOR_VIS.items():
    draw_pattern(name, defn['states'], defn['transitions'], defn['start'], defn['accept'])
