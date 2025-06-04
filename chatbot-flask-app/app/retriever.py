from dotenv import load_dotenv
import os
from langchain_postgres.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()

def retrieve_similar_chunks(query, k=3):
    db_name = os.getenv("db-name")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    pgname = os.getenv("pgname")
    collection_name = "state_of_union_vectors"
    connection_string = f"postgresql+psycopg2://{pgname}:{password}@{host}:{port}/{db_name}"

    openai_api_key = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-ada-002")
    db = PGVector.from_existing_index(
        embedding=embeddings,
        collection_name=collection_name,
        connection=connection_string
    )
    similar = db.similarity_search_with_score(query, k=k)
    print(similar)
    return similar

# Example usage:
# if __name__ == "__main__":
# query = "what is a healing ulcer?"
# #     results = retrieve_similar_chunks(query, k=3)
# #     print(results)
# retrieve_similar_chunks(query,k=2)