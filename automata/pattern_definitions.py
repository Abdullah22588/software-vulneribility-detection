# -----------------------------------------------------
# File: automata/pattern_definitions.py
# Purpose: Define vulnerability patterns for automaton
# -----------------------------------------------------

# Token-based patterns used by your finite automaton detector
PATTERN_LIST = {
    "SQL Injection": {
        "states": ["state0", "state1", "state2", "vulnerable"],
        "start": "state0",
        "accept": ["vulnerable"],
        "transitions": [
            ("state0", "execute", "state1"),
            ("state1", "(", "state2"),
            ("state2", "+", "vulnerable")  # concatenation means injection
        ],
    },

    "Hardcoded Password": {
        "states": ["state0", "state1", "state2", "vulnerable"],
        "start": "state0",
        "accept": ["vulnerable"],
        "transitions": [
            ("state0", "password", "state1"),
            ("state1", "=", "state2"),
            ("state2", "'", "vulnerable")
        ],
    },
}


# 👇 This is what your main.py is looking for (for visualization)
PATTERN_LIST_FOR_VIS = {
    "SQL Injection": {
        "states": ["start", "input_received", "concat", "vulnerable"],
        "start": "start",
        "accept": ["vulnerable"],
        "transitions": [
            ("start", "input", "input_received"),
            ("input_received", "+", "concat"),
            ("concat", "SQL", "vulnerable"),
        ],
    },

    "Hardcoded Password": {
        "states": ["start", "assign", "quote", "vulnerable"],
        "start": "start",
        "accept": ["vulnerable"],
        "transitions": [
            ("start", "password", "assign"),
            ("assign", "=", "quote"),
            ("quote", "'", "vulnerable"),
        ],
    },
}
