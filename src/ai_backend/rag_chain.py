from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from src.ai_backend.vector_loader import collection


def create_rag_chain():
    llm = ChatOpenAI(temperature=0)
    vector_store = Chroma(collection_name="argo_metadata")
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(),
        return_source_documents=True
    )
    return qa

def query_argo_rag(user_query):
    qa = create_rag_chain()
    response = qa.run(user_query)
    return response
