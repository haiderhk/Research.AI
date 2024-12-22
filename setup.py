import os, getpass


def set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


set_env('GROQ_API_KEY')
set_env("TAVILY_API_KEY")
set_env('LANGCHAIN_API_KEY')
os.environ["LANCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "ResearchAI"