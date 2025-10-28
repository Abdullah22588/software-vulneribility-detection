# visualizer/automata_visualizer.py
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"


def draw_pattern(name, states, transitions, start, accept, output_dir='results'):
    dot = Digraph(comment=name)
    dot.attr(rankdir='LR', size='8,5')

    # nodes
    for s in states:
        if s in accept:
            dot.node(s, shape='doublecircle')
        else:
            dot.node(s, shape='circle')

    # start arrow
    dot.node('start', label='', shape='point')
    dot.edge('start', start)

    # transitions: transitions is list of (from, symbol, to)
    for (a, symbol, b) in transitions:
        # label small -> use symbol as label
        dot.edge(a, b, label=symbol)

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{name.replace(' ','_')}.gv")
    dot.render(filename, format='png', cleanup=True)
    print(f"🎨 Pattern visual saved to {filename}.png")
