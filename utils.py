import base64
from pathlib import Path

def save_image(graph):
    with open("assets/human-in-the-loop.png", "wb") as fout:
        fout.write(graph.get_graph().draw_mermaid_png())
        print("Graph Image saved!")