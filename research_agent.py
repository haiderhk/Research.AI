from create_analysts_graph import create_analysts_graph
from IPython.display import Markdown


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
else:
    create_analysts_graph.invoke(None, thread)

final_state = create_analysts_graph.get_state(thread)
analysts = final_state.values.get("analysts")

print("\n\n\t\t***** FINAL ANALYSTS *****\n")
for analyst in analysts:
    print(analyst.persona)



