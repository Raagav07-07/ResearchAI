from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent,AgentExecutor
from pydantic import BaseModel
from tools import duck_search,savetool
load_dotenv()
class ResearchResponse(BaseModel):
    title:str
    summary:str
    sources:list[str]
    toolsUsed:list[str]
llm=ChatGroq(model="llama3-70b-8192")
parser=PydanticOutputParser(pydantic_object=ResearchResponse)
prompt=ChatPromptTemplate.from_messages(
    [
        ('system',
         """
You are a research agent helping me to generate a research paper. Answer the user query and use necessary tools.
wrap the output in this format and provide no other text \n{format_instruction}
"""),
("placeholder",'{chat_history}'),
("human","{query}"),
("placeholder",'{agent_scratchpad}')
    ]
).partial(format_instruction=parser.get_format_instructions())
agent=create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[duck_search,savetool]
)
agent_executor=AgentExecutor(agent=agent,tools=[duck_search,savetool],verbose=True)
query_input=input("How can i help you?")
raw_output=agent_executor.invoke({"query":query_input})
print(raw_output)
