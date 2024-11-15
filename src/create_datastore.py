import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WEBSITE_URL = "https://www.promtior.ai/service"


TEXT_FILE_PATH = os.path.join(CURRENT_DIR, "data", "aboutPromtior.txt")
VECTOR_STORE_PATH = os.path.join(CURRENT_DIR, "vectorstore")


def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    return save_to_chroma(documents)

def load_documents():
    doc_text = load_text_content()
    doc_web = load_web_content(WEBSITE_URL)
    return doc_text + doc_web

def load_text_content():
    loader = TextLoader(TEXT_FILE_PATH)
    documents = loader.load()
    return documents

def load_web_content(url):
    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter()
    chunks = text_splitter.split_documents(documents)
    return chunks

def save_to_chroma(chunks):
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=VECTOR_STORE_PATH,
    )
    return db

if __name__ == "__main__":
    main()