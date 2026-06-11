from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI 
from tavily import  TavilyClient
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
import os


def tavily_key():
    tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
   )
    return tavily_client

def get_model():
    return ChatMistralAI(model = "mistral-small-latest", temperature=0.4)

def chunk_transcribe(transcribe : str) -> list:
     spliting = RecursiveCharacterTextSplitter(
        chunk_size = 350,
        chunk_overlap = 50
    )
     return spliting.split_text(transcribe)

class FactCheckResult(BaseModel):
       verdict: str
       confidence: int
       reason: str

def fake_detection(transcribe : str) ->str :
    llm = get_model()
    chunks = chunk_transcribe(transcribe)
    tavily_api_key = tavily_key()

    prompt = ChatPromptTemplate.from_messages([
        
    ("system",
     """
     You are a fact-checking agent.

     Always search the web before giving a verdict.
     Return output in this format:
            {format_instructions}
     Return:
     - verdict
     - confidence
     - explanation
     {tavily_result}
     """),
    ("human", "{input}")
    ])

    parser = PydanticOutputParser(pydantic_object=FactCheckResult)

    combine = []
    for chunk in chunks:
        web_result = tavily_api_key.search(
             query = chunk[:400]
          )
        
        chain = prompt | llm
        
        response = chain.invoke({
            "input":chunk,
            "tavily_result":"\n\n".join(web_result),
            "format_instructions": parser.get_format_instructions()
        })
        result = parser.parse(response.content)
        combine.append(result)

        return combine

   
    






