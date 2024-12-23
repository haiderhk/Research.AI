from schemas import InterviewState
from utils import save_image, route_messages_condition
from nodes import generate_question, generate_answer, search_web, search_wikipedia, write_section, save_interview


from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver


interview_builder = StateGraph(InterviewState)
interview_builder.add_node("Ask Question", generate_question)
interview_builder.add_node("Search Web", search_web)
interview_builder.add_node("Search Wikipedia", search_wikipedia)
interview_builder.add_node("Answer Question", generate_answer)
interview_builder.add_node("Save Interview", save_interview)
interview_builder.add_node("Write Section", write_section)


interview_builder.add_edge(START, "Ask Question")
interview_builder.add_edge("Ask Question", "Search Web")
interview_builder.add_edge("Ask Question", "Search Wikipedia")
interview_builder.add_edge("Search Web", "Answer Question")
interview_builder.add_edge("Search Wikipedia", "Answer Question")
interview_builder.add_conditional_edges("Answer Question", route_messages_condition, ["Ask Question", "Save Interview"])
interview_builder.add_edge("Save Interview", "Write Section")
interview_builder.add_edge("Write Section", END)

memory = MemorySaver()

interview_graph = interview_builder.compile(checkpointer = memory).with_config(run_name = "Conduct Interviews")

save_image(interview_graph, path = "assets/interview_graph.png")