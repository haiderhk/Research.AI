import operator
from typing import List, Annotated
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph.message import MessagesState




class Analyst(BaseModel):
    affiliation: str = Field(description = "Primary affiliation of the analyst.")
    name: str = Field(description = "Name of the analyst.")
    role: str = Field(description = "Role of the analyst in the context of the topic.")
    description: str = Field(description = "Description of the analyst's focus, concerns, and motives")

    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"
    


class Perspectives(BaseModel):
    analysts: List[Analyst] = Field(description = "Comprehensive list of all analysts with their roles and affiliations.")



class GenerateAnalystsState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str #Human feedback for human-in-the-loop
    analysts: List[Analyst]


class InterviewState(MessagesState):
    max_num_turns: int
    context: Annotated[List, operator.add] # The external information retrieved
    analyst: Analyst
    interview: str # Interview transcript
    sections: list # For Send()

class SearchQuery(BaseModel):
    search_query: str = Field(None, description = "Search query for retrieval")


class ResearchGraphState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str #Human feedback for human-in-the-loop
    analysts: List[Analyst]
    sections: Annotated[List, operator.add] # For compiling all sections from different analysts.
    introduction: str # Introduction for the final compiled report
    content: str
    conclusion: str
    final_report: str