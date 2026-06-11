import os 
from langchain_chroma import Chroma 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings 


def embedding_model():
    return NVIDIAEmbeddings(model="nvidia/nv-embed-v1",
                            nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
                            model_kwargs = {"device" : 'cpu'})

def vector_stores(transcribe : str) -> Chroma:
    spliting = RecursiveCharacterTextSplitter(
         chunk_size=3000,
         chunk_overlap=200
    )
    chunks = spliting.split_text(transcribe)

    embedding = embedding_model()

    docs = [
             Document(page_content=chunk, meta_data = {"index":i})
             for i,chunk in enumerate(chunks)
             ]
    
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding= embedding,
        persist_directory="chroma_db",
        collection_name="metting_camp"
    )

    return vector_db

def load_db() -> Chroma:
    embedding = embedding_model()
    vector_db = Chroma(
        embedding_function = embedding,
        persist_directory="chroma_db",
        collection_name="metting_camp"
    )

    return vector_db

def retrivers(vectors : Chroma, k : int = 4):
    return vectors.as_retriever(
        search_type = "mmr",
        kwargs={"k" : k}
    )

 




