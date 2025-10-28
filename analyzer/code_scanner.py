# -----------------------------------------------
# File: analyzer/code_scanner.py
# Purpose: Extract tokens from code files
# -----------------------------------------------

import re

def tokenize_code(code):
    """
    Convert code into a list of simplified tokens.
    """
    tokens = re.findall(r'[A-Za-z_]+|[=+*/()]|\"', code)
    return tokens

def read_code_file(file_path):
    """
    Read source code file content.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
