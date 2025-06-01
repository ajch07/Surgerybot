from flask import current_app
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PostgreSQLVectorStore
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from sqlalchemy.orm import sessionmaker
from .db import get_db_session

class RAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = PostgreSQLVectorStore(
            embeddings=self.embeddings,
            connection_string=current_app.config['DATABASE_URL']
        )
        self.llm = OpenAI(model_name="gpt-3.5-turbo")
        self.retrieval_qa = RetrievalQA(
            llm=self.llm,
            retriever=self.vector_store.as_retriever()
        )

    def generate_response(self, query):
        return self.retrieval_qa.run(query)

    def add_document(self, document_text):
        vector = self.embeddings.embed(document_text)
        self.vector_store.add_documents([{
            "text": document_text,
            "vector": vector
        }])