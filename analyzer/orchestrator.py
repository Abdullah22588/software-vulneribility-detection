# analyzer/orchestrator.py
from analyzer.ast_detector import analyze_file as ast_analyze
from automata.finite_automata import FiniteAutomata
from automata.pattern_definitions import PATTERN_LIST  # token-based patterns if needed
from analyzer.code_scanner import tokenize_code, read_code_file

def run_hybrid_scan(path):
    results = []
    # 1) AST-based (python only)
    if path.endswith('.py'):
        results += ast_analyze(path)

    # 2) Token/Automata-based (language-agnostic)
    code = read_code_file(path)
    tokens = tokenize_code(code)
    for vuln_name, details in PATTERN_LIST.items():
        fa = FiniteAutomata(details['states'], details['start'], details['accept'], details['transitions'])
        if fa.process_input(tokens):
            results.append(f"⚠️  Vulnerability Detected (automata): {vuln_name} in {path}")
    if not results:
        results.append(f"✅  No known vulnerabilities detected in {path}")
    return results
