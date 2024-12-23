import base64
from pathlib import Path
from langgraph.graph import END
from langchain_core.messages import AIMessage

from schemas import GenerateAnalystsState, InterviewState


def save_image(graph, path):
    with open(path, "wb") as fout:
        fout.write(graph.get_graph().draw_mermaid_png())
        print("Graph Image saved!")


def save_markdown(markdown_content: str, filename: str = "assets/report.md"):
    """
    Save markdown content to a file.
    
    Args:
        markdown_content: The markdown string to save
        filename: Name of the output file (default: output.md)
    """
    with open(filename, 'w') as f:
        f.write(markdown_content)
    print(f"Markdown saved to: {filename}")


def should_continue_condition(state: GenerateAnalystsState):
    """Return the next node to execute based on human feedback"""
    human_analyst_feedback = state.get("human_analyst_feedback", None)

    if human_analyst_feedback:
        return "Create Analysts"
    else:
        END


def route_messages_condition(state: InterviewState, name: str = "expert"):
    messages = state["messages"]
    max_num_turns = state.get("max_num_turns", 2)

    num_responses = 0
    for message in messages:
        if isinstance(message, AIMessage) and message.name == name:
            num_responses += 1

    if num_responses >= max_num_turns:
        return "Save Interview"
    
    last_question = messages[-2]

    if "Thank you for your help" in last_question.content:
        return "Save Interview"
    
    return "Ask Question"



