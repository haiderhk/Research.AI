from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()


llm = ChatGroq(model = "lama3-8b-8192", temperature=0)

