# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:10:13 2024

@author: snandanw
More on Chains -  Sequence of Chains
"""

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

model =  ChatOpenAI(temperature = 0.5)

message = [("system","You are a comedian who tells a joke about {topic}"),
           ("human","Tell me {joke_count} jokes")]

prompt = ChatPromptTemplate.from_messages(message)

# say we want to add some more additional steps to the chain, then we can do it through Runnables

uppercase_opt = RunnableLambda(lambda x: x.upper())
count_words = RunnableLambda(lambda x: f'Word Count : {len(x.split())}\n{x}')

# Create the combined chain using Langchain Expression Language (LCEL)
chain = prompt | model | StrOutputParser() | uppercase_opt | count_words


# Run the Chain
result = chain.invoke({"topic":"lawyer" , "joke_count":2})

print(result)
