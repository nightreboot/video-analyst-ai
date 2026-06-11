from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

def get_model():
    return ChatMistralAI(model = "mistral-small-latest", temperature=0.4)

def building_prompt(prompt : str) -> str:
    llm = get_model()

    different_prompt = (RunnablePassthrough() | RunnableLambda(lambda x : {"text":x}) | 
    ChatPromptTemplate.from_messages([
        ('system',prompt),
        ('human','{text}')
    ]) | llm | StrOutputParser()
    )
    return different_prompt


def action_items(transcript:str)->str:
    chain = building_prompt(
         "You are an expert meeting analyst. From the meeting transcript, "
        "extract all action items. For each provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'Not specified')\n\n"
        "Format as a numbered list. If none found say 'No action items found.'"
    )

    return chain.invoke(transcript)

def key_dicision(transcript : str) -> str:
    chain = building_prompt(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all key decisions made. Format as a numbered list. "
        "If none found say 'No key decisions found.'"
    )
    return chain.invoke(transcript)

def questions(transcript: str) -> str:
    chain = building_prompt(
        "From the meeting transcript, extract all unresolved questions "
        "or topics needing follow-up. Format as a numbered list. "
        "If none found say 'No open questions found.'"
    )
    return chain.invoke(transcript)
