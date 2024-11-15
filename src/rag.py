import os
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_STORE_PATH = os.path.join(CURRENT_DIR, "vectorstore")
PROMPT_TEMPLATE = """
You are a question answering task assistant for Promptior company. 
Use the following pieces of recovered context to answer the question.
If you don't know the answer, say that you don't know 
Use three sentences maximum and keep the concise answers
\n\n
{context}

---

Question: {question}
"""


def get_rag_chain():
    embeddings = OpenAIEmbeddings()

    vectorstore = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    model = ChatOpenAI()
    
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return rag_chain


def format_docs(docs):
    response_text = "\n\n".join(doc.page_content for doc in docs)
    return response_text


rag_chain = get_rag_chain()
