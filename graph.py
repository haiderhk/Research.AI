from nodes import create_analysts, human_feedback, should_continue_condition
from schemas import GenerateAnalystsState
from utils import save_image

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver



builder = StateGraph(GenerateAnalystsState)

builder.add_node("Create Analysts", create_analysts)
builder.add_node("Human Feedback", human_feedback)

builder.add_edge(START, "Create Analysts")
builder.add_edge("Create Analysts", "Human Feedback")
builder.add_conditional_edges("Human Feedback", should_continue_condition)

memory = MemorySaver()

graph = builder.compile(interrupt_before=["Human Feedback"], checkpointer=memory)

# save_image(graph)

