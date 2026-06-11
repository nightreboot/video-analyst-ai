from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

def get_model():
    return ChatMistralAI(model = "mistral-small-latest", temperature=0.4)

def chunking_of_transcibe(transcribe : str) -> list:
    spliting = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )
    return spliting.split_text(transcribe)

def summarize_text(transcribe : str) -> str:
    llm = get_model()
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Summarize this portion of a meeting transcript concisely'),
        ('human','{text}')
    ])

    chain = prompt | llm | StrOutputParser()
    

    chunks = chunking_of_transcibe(transcribe)

    summarize_chunk = [chain.invoke(({"text" : chunk}for chunk in chunks))]

    combination = "\n\n".join(summarize_chunk)

    prompt2 =  ChatPromptTemplate.from_messages([
        ('system', "You are an expert meeting summarizer. Combine these partial summaries "
            "into one final professional meeting summary in bullet points.",),
        ('human','{text}')
    ])

    runnables = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text" : x}) | prompt2 | 
        llm | StrOutputParser()
    ) 
     
    return runnables.invoke(combination) 

def title_generator(transcribe : str) -> str:
    llm = get_model()

    title_creater = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | 
        ChatPromptTemplate.from_messages([
            (
             "system",
                "Based on the meeting transcript, generate a short professional meeting title "
                "(max 8 words). Only return the title, nothing else.",
            ),
            ("human", "{text}"),
            ]) | llm | StrOutputParser()
    ) 
     
    return title_creater.invoke(transcribe[:2000]) 












