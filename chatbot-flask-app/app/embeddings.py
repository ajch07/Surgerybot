from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import numpy as np
import psycopg2
from your_embedding_library import embed_text  # Replace with the actual embedding library

Base = declarative_base()

def get_db_connection():
    connection = psycopg2.connect(
        dbname='your_db_name',
        user='your_db_user',
        password='your_db_password',
        host='your_db_host',
        port='your_db_port'
    )
    return connection

def embed_and_store_data(text_data):
    # Generate embeddings for the text data
    embeddings = embed_text(text_data)
    
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Store embeddings in the PostgreSQL vector database
    for embedding in embeddings:
        cursor.execute(
            "INSERT INTO your_vector_table (embedding) VALUES (%s)",
            (np.array(embedding),)
        )
    
    connection.commit()
    cursor.close()
    connection.close()