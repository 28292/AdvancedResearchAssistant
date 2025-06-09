# document_search.py

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.documents import Document

# Build Vector Store
def build_vector_store_from_docs(docs):
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)
    db = FAISS.from_documents(split_docs, OpenAIEmbeddings())
    return db

# Create QA Chain
def build_qa_chain(db, temperature=0.3):
    retriever = db.as_retriever(search_type="similarity", k=5)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, return_source_documents=True)
    return chain

# Ask a question
def ask_question(chain, question, chat_history=[]):
    result = chain({"question": question, "chat_history": chat_history})
    return result["answer"], result.get("source_documents", [])
