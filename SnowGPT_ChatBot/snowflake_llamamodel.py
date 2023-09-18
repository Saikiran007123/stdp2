from llama_index import Document
import snowflake.connector
from config import *
import openai
import streamlit as st
from langchain.document_loaders import UnstructuredURLLoader
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
import os
import openai
openai.api_key = "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"
os.environ["OPENAI_API_KEY"] = "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"

conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema
)
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT GET_PRESIGNED_URL(@snowgpt_s3_stage, METADATA$FILENAME) FROM @snowgpt_s3_stage")
file_list = cursor.fetchall()
presigned_urls = [row[0] for row in file_list]

# print(presigned_urls)


loader = UnstructuredURLLoader(urls=presigned_urls)
documents = loader.load()
# st.write("Documents : ",len(documents))

print(len(documents))

# def split_docs(documents,chunk_size=500,chunk_overlap=20):
#   text_splitter= RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
#   docs=text_splitter.split_documents(documents)
#   return docs
# docs=split_docs(documents)
# # st.write("Vectors : ",len(docs))


# embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

document = SimpleDirectoryReader('s3://snowgptfiles').load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

response = query_engine.query("What is this text about?")
print(response)

cursor.close()
conn.close()


