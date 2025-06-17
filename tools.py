from langchain_core.tools import Tool
from langchain_community.tools import WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime
def save_to_txt(data:str,filename:str="research.txt"):
    time=datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
    text=f"\nResearch Output\n{time}\n\n{data}\n\n"
    with open(filename,"a",encoding="utf-8") as f:
        f.write(text)
savetool=Tool(
    name="savetool",
    func=save_to_txt,
    description="Saving the structured format to a file"
)
search=DuckDuckGoSearchRun()
duck_search=Tool(
    name="Search",
    func=search.run,
    description="Search the web for information"
)
