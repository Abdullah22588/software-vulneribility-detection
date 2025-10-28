# analyzer/ast_detector.py
import ast
import os

def is_string_literal(node):
    return isinstance(node, ast.Constant) and isinstance(node.value, str) \
           or isinstance(node, ast.Str)

def expr_is_concat(node):
    # True if node is a binary addition (string + var) or nested adds
    return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add)

def expr_is_percent_format(node):
    # True if node is a binary Mod operation: "..." % var
    return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod)

def expr_is_fstring(node):
    return isinstance(node, ast.JoinedStr)

def contains_name(node):
    # returns True if any Name node exists inside
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            return True
    return False

def get_assignments(tree):
    # Map variable name -> assigned AST node (last assignment wins)
    assigns = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                assigns[target.id] = node.value
    return assigns

def detect_hardcoded_passwords(tree):
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                varname = target.id.lower()
                if 'pass' in varname:  # heuristic
                    if is_string_literal(node.value):
                        findings.append(("Hardcoded Password", node.lineno, varname))
    return findings

def detect_sql_injection(tree):
    findings = []
    assigns = get_assignments(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr.lower() == 'execute':
                # If execute has more than 1 positional arg, treat as parameterized -> safe
                if len(node.args) >= 2:
                    continue
                # If execute is called with keyword params/parameters, consider safe
                kw_names = {kw.arg.lower() if kw.arg else '' for kw in node.keywords}
                if 'params' in kw_names or 'parameters' in kw_names:
                    continue

                # analyze first argument (query)
                if not node.args:
                    continue
                arg0 = node.args[0]

                # Case A: direct concatenation passed to execute: "..." + var
                if expr_is_concat(arg0) and contains_name(arg0):
                    findings.append(("SQL Injection (string concat formatting)", node.lineno))
                    continue

                # Case B: direct f-string passed: f"...{var}..."
                if expr_is_fstring(arg0) and contains_name(arg0):
                    findings.append(("SQL Injection (f-string passed to execute)", node.lineno))
                    continue

                # Case C: percent-format passed inline: "..." % var
                if expr_is_percent_format(arg0) and contains_name(arg0):
                    findings.append(("SQL Injection (percent-format passed to execute)", node.lineno))
                    continue

                # Case D: a named variable is passed; inspect the variable's assignment
                if isinstance(arg0, ast.Name):
                    var_name = arg0.id
                    assigned = assigns.get(var_name)
                    if assigned is None:
                        continue
                    # If the variable is a plain string literal -> safe
                    if is_string_literal(assigned):
                        continue
                    # If variable assigned via concatenation that includes names -> vulnerable
                    if expr_is_concat(assigned) and contains_name(assigned):
                        findings.append((f"SQL Injection (concat in variable '{var_name}')", assigned.lineno if hasattr(assigned, 'lineno') else node.lineno))
                        continue
                    # If variable assigned via percent-format with name -> vulnerable
                    if expr_is_percent_format(assigned) and contains_name(assigned):
                        findings.append((f"SQL Injection (percent-format in '{var_name}')", assigned.lineno if hasattr(assigned, 'lineno') else node.lineno))
                        continue
                    # If variable is f-string -> vulnerable
                    if expr_is_fstring(assigned) and contains_name(assigned):
                        findings.append((f"SQL Injection (f-string in '{var_name}')", assigned.lineno if hasattr(assigned, 'lineno') else node.lineno))
                        continue

                # Otherwise, no clear unsafe pattern found for this execute call
    return findings

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        src = f.read()
    try:
        tree = ast.parse(src, filename=filepath)
    except SyntaxError as e:
        return [f"⚠️  Could not parse {os.path.basename(filepath)}: {e}"]

    results = []

    # Hardcoded password detection
    hp = detect_hardcoded_passwords(tree)
    for name, lineno, var in hp:
        results.append(f"⚠️  Vulnerability Detected: {name} in {os.path.basename(filepath)} at line {lineno} (variable: {var})")

    # SQL injection detection
    si = detect_sql_injection(tree)
    for item in si:
        if isinstance(item, tuple):
            findings_name, lineno = item
            results.append(f"⚠️  Vulnerability Detected: {findings_name} in {os.path.basename(filepath)} at line {lineno}")
        else:
            results.append(f"⚠️  Vulnerability Detected: SQL Injection in {os.path.basename(filepath)}")

    if not results:
        results.append(f"✅  No known vulnerabilities detected in {os.path.basename(filepath)}")
    return results
