from utils import save_markdown
from interview_graph import interview_graph
from create_analysts_graph import create_analysts_graph

from IPython.display import Markdown
from langchain_core.messages import HumanMessage


max_analysts = 3
topic = input("Enter area of research: ")

thread = {"configurable": {"thread_id": "1"}}

for event in create_analysts_graph.stream({
    "topic": topic,
    "max_analysts": max_analysts,
}, thread, stream_mode = "values"):
    analysts = event.get("analysts", '')
    if analysts:
        print("\nThe analysts generated so far: \n")
        for analyst in analysts:
            print(analyst.persona)
            print("------------------------------------------")


human_analyst_feedback = input("Would you like to update any of the analysts? (Type \"no\" to exit) ")

if human_analyst_feedback.lower() != "no":
    create_analysts_graph.invoke({"human_analyst_feedback": human_analyst_feedback}, thread)
    # for event in create_analysts_graph.stream({
    #     "human_analyst_feedback": human_analyst_feedback
    # }, thread, stream_mode = "values"):
        # analysts = event.get('analysts', '')
        # if analysts:
            # for analyst in analysts:
                # print(analyst.persona)
                # print("------------------------------------------")
# else:
#     create_analysts_graph.invoke(None, thread)

final_state = create_analysts_graph.get_state(thread)
analysts = final_state.values.get("analysts")

print("\n\n\t\t***** FINAL ANALYSTS *****\n")
for analyst in analysts:
    print(analyst.persona)


conduct_interview_message = HumanMessage(f"So you said you were writing an article on {topic}?")
messages = [conduct_interview_message]


#Checking the interview for a single analyst
interview = interview_graph.invoke({"analyst": analysts[0], "messages": messages, "max_num_turns": 2}, thread)

generated_report_section = interview['sections'][0]

save_markdown(generated_report_section)

print(f"Finished interview with the section: \n\n{generated_report_section}")

