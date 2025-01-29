from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model = "deepseek-r1:7b", temperature = 0)
llm_json_mode = ChatOllama(model = "deepseek-r1:7b", temperature= 0, format = "json")

# for event in llm.stream(["Write the python code for a function that creates a pyramid pattern out of asterisks."]):
#     print(event.content, end = "")

