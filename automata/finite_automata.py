# -----------------------------------------------
# File: automata/finite_automata.py
# Purpose: Core Finite Automata implementation
# -----------------------------------------------

class FiniteAutomata:
    def __init__(self, states, start_state, accept_states, transitions):
        """
        Initialize the automaton.
        :param states: list of states
        :param start_state: initial state
        :param accept_states: list of final states
        :param transitions: dictionary { (state, symbol): next_state }
        """
        self.states = states
        self.start_state = start_state
        self.current_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def reset(self):
        """Reset the automaton to its start state."""
        self.current_state = self.start_state

    def process_symbol(self, symbol):
        """Process a single input symbol."""
        key = (self.current_state, symbol)
        if key in self.transitions:
            self.current_state = self.transitions[key]
        return self.current_state

    def process_input(self, input_sequence):
        """Process a full list of input symbols."""
        self.reset()
        for symbol in input_sequence:
            self.process_symbol(symbol)
        return self.is_accepted()

    def is_accepted(self):
        """Check if automaton reached an accept state."""
        return self.current_state in self.accept_states
