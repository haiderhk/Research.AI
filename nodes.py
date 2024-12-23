from initialize_groq import llm
from prompts import analyst_instructions, question_instructions
from schemas import GenerateAnalystsState, Perspectives, InterviewState

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END

def create_analysts(state: GenerateAnalystsState):
    """Create analysts"""
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback", "")

    structured_llm = llm.with_structured_output(Perspectives)

    system_message_prompt = analyst_instructions.format(
        topic = topic,
        max_analysts = max_analysts,
        human_analyst_feedback = human_analyst_feedback
    )
    
    system_message = SystemMessage(system_message_prompt)
    human_message  = HumanMessage("Generate the list of analysts.")

    analysts = structured_llm.invoke([system_message] + [human_message])
    

    return {"analysts": analysts.analysts}



def human_feedback(state: GenerateAnalystsState):
    """Node to be interrupted upon for human input"""
    pass


def should_continue_condition(state: GenerateAnalystsState):
    """Return the next node to execute based on human feedback"""
    human_analyst_feedback = state.get("human_analyst_feedback", None)

    if human_analyst_feedback:
        return "create_analysts"
    else:
        END


def generate_question(state: InterviewState):
    """Node to generate a question for the analyst to ask"""

    analyst = state["analyst"]
    messages = state["messages"]

    system_message = SystemMessage(question_instructions.format(goals = analyst.persona))
    question = llm.invoke([system_message] + messages)

    return {"messages": question}



    
