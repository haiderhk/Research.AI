from typing import List
from typing_extensions import TypedDict
from pydantic import BaseModel, Field




class Analyst(BaseModel):
    affiliation: str = Field("Primary affiliation of the analyst.")
    name: str = Field("Name of the analyst.")
    role: str = Field("Role of the analyst in the context of the topic.")
    description: str = Field("Description of the analyst's focus, concerns, and motives")

    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"
    


class Perspectives(BaseModel):
    analysts: List[Analyst] = Field("Comprehensive list of all analysts with their roles and affiliations.")



class GenerateAnalystsState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str #Human feedback for human-in-the-loop
    analysts: List[Analyst]