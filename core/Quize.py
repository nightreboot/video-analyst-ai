from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()
import os


def get_model():
    return ChatMistralAI(
        api_key=os.getenv("MISTRAL_API_KEY"),
        model="mistral-small-latest",
        temperature=0.3
    )


def chunk_transcribe(transcribe: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )
    return splitter.split_text(transcribe)


def Quize(transcribe: str) -> str:
    llm = get_model()

    prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert quiz generator.

Read the given text and create a quiz based only on important information.

Rules:
- Create clear MCQ questions.
- Each question must have 4 options and 1 correct answer.
- Avoid repeated or irrelevant questions.
- If no meaningful quiz can be generated, return None.

Return output in JSON format:

{{
  "quiz": [
    {{
      "question": "",
      "options": ["", "", "", ""],
      "correct_answer": ""
    }}
  ]
}}
"""
    ),
    (
        "human",
        "Text:\n{text}"
    )
])

    chain = prompt | llm | StrOutputParser()

    chunks = chunk_transcribe(transcribe)
    combine = []

    for chunk in chunks:
        response = chain.invoke({
            "text": chunk
        })
        combine.append(response)

    return "\n\n".join(combine)
 
    

