# -*- coding: utf-8 -*-
"""
Created on Sat May 18 12:48:16 2024

@author: snandanw
"""

import os
import langchain
import streamlit as st
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader
#from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain

load_dotenv()

#pdf_path = "..\RAG_SWAP"
#print(pdf_path)

pdf_path =  "..\RAG"
print(f"PDF Path: {pdf_path}")
llm = OpenAI(temperature= 0.6, max_tokens=1000)


# In my project it was basically pdfs that I wanted extract text of
def load_documents(pdf_path):
    loader = PyPDFDirectoryLoader(pdf_path)
    data = loader.load()
    
    return data

data = load_documents(pdf_path)
print(len(data), type(data), data[:2])


###############################################################

def create_chucks():
    data = load_documents(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n', '\n', '.', ','], 
                                                   chunk_size=600,
                                                   chunk_overlap=100,
                                                   )
    docs = text_splitter.split_documents(data)
    return docs
print(create_chucks)

docs = create_chucks()
print(len(docs), type(docs), docs[:2])
embeddings = OpenAIEmbeddings()
# To create Vector embedding we need to run below statement.
# But as I have already created Embeddings and stored previously hence I will just Load that
#vectorstore_openai = FAISS.from_documents(docs, embeddings)
#vectorindex_openapi =FAISS.load_local("vector_index", embeddings)

vectorindex_openapi = FAISS.from_documents(docs, embedding=embeddings)


### If We use PineCone then perform following steps-

## Vector Search DB In Pinecone


st.header("Q&A Chatbot")


query = st.chat_input("Enter Your Query ")



if query:
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorindex_openapi.as_retriever())
    result = chain({"question": query}, return_only_outputs=True)
    st.header("Query...")
    st.write(query)
    st.header("Answer")
    st.write(result["answer"])
    

# This is working   


