from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
load_dotenv()

# loader = TextLoader('../../SRB’s Manual of Surgery.txt', encoding='utf-8')
# documents = loader.load()

# # Let's say each document corresponds to one page, starting from page 13
# start_page = 13
# for i, doc in enumerate(documents):
#     doc.metadata["page_number"] = start_page + i

# print(documents)  # {'source': '../../SRB’s Manual of Surgery.txt', 'page_number': 13}


# text_splitter=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=300)
# text=text_splitter.split_documents(documents)
# print(text)


def load_pdf_with_page_metadata(pdf_path, start_page=1, end_page=None):
    reader = PdfReader(pdf_path)
    docs = []
    # Adjust for 0-based indexing
    start = start_page - 1
    end = end_page if end_page else len(reader.pages)
    for i in range(start, end):
        page = reader.pages[i]
        text = page.extract_text()
        if text:
            docs.append(Document(page_content=text, metadata={"page_number": i + 1}))
    return docs

# --- CONFIG ---
pdf_path = "../../SRB’s Manual of Surgery.pdf"
start_page = 13
end_page = 27

# --- LOAD PDF PAGES AS DOCUMENTS ---
documents = load_pdf_with_page_metadata(pdf_path, start_page=start_page, end_page=end_page)
print(f"Loaded {len(documents)} pages from PDF.")

# --- SPLIT EACH PAGE INTO CHUNKS, PRESERVING PAGE NUMBER ---
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
chunks = []
for doc in documents:
    for chunk in text_splitter.split_text(doc.page_content):
        # Each chunk gets the original page's metadata
        chunks.append(Document(page_content=chunk, metadata=doc.metadata.copy()))

print(f"Total chunks: {len(chunks)}")
print("Sample chunk metadata:", chunks[0].metadata)
print(chunks)


openai_api_key = os.getenv("OPENAI_API_KEY")
if(openai_api_key):
    print(True)
embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key,model="text-embedding-ada-002")
vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
# print(vectors)

db_name=os.getenv("db-name")
password=os.getenv("password")
host=os.getenv("host")
port=os.getenv("port")
pgname=os.getenv("pgname")
print(pgname)
from langchain_postgres.vectorstores import PGVector
connection_string = f"postgresql+psycopg2://{pgname}:{password}@{host}:{port}/{db_name}" 
collection_name="state_of_union_vectors"
print(connection_string)

db=PGVector.from_documents(documents=chunks,embedding=embeddings,collection_name=collection_name,connection=connection_string)