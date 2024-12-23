from initialize_groq import llm
from utils import should_continue_condition, route_messages_condition
from schemas import GenerateAnalystsState, Perspectives, InterviewState, SearchQuery
from prompts import analyst_instructions, question_instructions, search_instructions, answer_instructions, section_writer_instructions

from langgraph.graph import END
from langchain_community.tools import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import SystemMessage, HumanMessage, get_buffer_string

tavily_search = TavilySearchResults(max_results=3)

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





def generate_question(state: InterviewState):
    """Node to generate a question for the analyst to ask"""

    analyst = state["analyst"]
    messages = state["messages"]

    system_message = SystemMessage(question_instructions.format(goals = analyst.persona))
    question = llm.invoke([system_message] + messages)

    return {"messages": question}



def search_web(state: InterviewState):
    """Retrieve documents from a web search"""

    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([search_instructions] + state["messages"])

    search_docs = tavily_search.invoke(search_query.search_query)

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}


def search_wikipedia(state: InterviewState):
    """Retrieve documents from Wikipedia"""

    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([search_instructions] + state["messages"])

    search_docs = WikipediaLoader(query = search_query.search_query, load_max_docs=2).load()

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]} 



def generate_answer(state: InterviewState):
    """Node to answer the analyst question"""

    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    system_message = SystemMessage(content = answer_instructions.format(goals = analyst, context = context))
    answer = llm.invoke([system_message] + messages)
    answer.name = "expert"

    return {"messages": [answer]}


def save_interview(state: InterviewState):
    """Save the interview transcript"""

    messages = state["messages"]

    # Convert the interview to a string
    interview = get_buffer_string(messages)

    return {"interview": interview}



def write_section(state: InterviewState):
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    system_message = SystemMessage(content = section_writer_instructions.format(focus = analyst.description))
    human_message = HumanMessage(content = f"Use this source to write your section: {context}")

    section = llm.invoke([system_message] + [human_message])

    return {"sections": [section.content]}
    