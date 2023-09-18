import snowflake.connector
from config import *
import openai
import streamlit as st
from langchain.document_loaders import DirectoryLoader
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema
)
cursor = conn.cursor()

stage_file_path = f'@{stage_name}/'



cursor.execute("SELECT DISTINCT GET_PRESIGNED_URL(@snowgpt_s3_stage, METADATA$FILENAME) FROM @snowgpt_s3_stage")
file_list = cursor.fetchall()
presigned_urls = [row[0] for row in file_list]

print(presigned_urls)

loader = UnstructuredURLLoader(urls=presigned_urls)
documents = loader.load()
st.write("Documents : ",len(documents))


def split_docs(documents,chunk_size=500,chunk_overlap=20):
  text_splitter= RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
  docs=text_splitter.split_documents(documents)
  return docs
docs=split_docs(documents)
st.write("Vectors : ",len(docs))


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

pinecone.init(
    api_key=api_key,
    environment=environment
)

index = Pinecone.from_documents(docs,embeddings,index_name=index_name)

def get_similar_docs(query,k=1,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

query = "what is this text about"
similar_docs = get_similar_docs(query)
st.write(similar_docs)


cursor.close()
conn.close()