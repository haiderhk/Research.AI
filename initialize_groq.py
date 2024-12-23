from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()


# llm = ChatGroq(model = "llama3-70b-8192", temperature=0)
llm = ChatGroq(model = "llama3-groq-70b-8192-tool-use-preview", temperature=0)

