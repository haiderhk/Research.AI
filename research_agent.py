from graph import graph


max_analysts = 3
topic = input("Enter area of research: ")

thread = {"configurable": {"thread_id": "1"}}

for event in graph.stream({
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
    for event in graph.stream({
        "human_analyst_feedback": human_analyst_feedback
    }, thread, stream_mode = "values"):
        analysts = event.get('analysts', '')
        if analysts:
            for analyst in analysts:
                print(analyst.persona)
                print("------------------------------------------")


graph.stream(None, thread, stream_mode="updates")
final_state = graph.get_state(thread)
analysts = final_state.values.get("analysts")

print("\n\nFINAL ANALYSTS\n")
for analyst in analysts:
    print(analyst.persona)
