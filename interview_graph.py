from schemas import InterviewState
from utils import save_image, route_messages_condition
from nodes import generate_question, generate_answer, search_web, search_wikipedia, write_section, save_interview


from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver


builder = StateGraph(InterviewState)
builder.add_node("Ask Question", generate_question)
builder.add_node("Search Web", search_web)
builder.add_node("Search Wikipedia", search_wikipedia)
builder.add_node("Answer Question", generate_answer)
builder.add_node("Save Interview", save_interview)
builder.add_node("Write Section", write_section)


builder.add_edge(START, "Ask Question")
builder.add_edge("Ask Question", "Search Web")
builder.add_edge("Ask Question", "Search Wikipedia")
builder.add_edge("Search Web", "Answer Question")
builder.add_edge("Search Wikipedia", "Answer Question")
builder.add_conditional_edges("Answer Question", route_messages_condition)
builder.add_edge("Save Interview", "Write Section")
builder.add_edge("Write Section", END)

memory = MemorySaver()

interview_graph = builder.compile(checkpointer = memory).with_config(run_name = "Conduct Interviews")

save_image(interview_graph, path = "assets/interview_graph.png")