# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 13:59:02 2024

@author: snandanw
More about Chains
"""

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema.output_parser import StrOutputParser
load_dotenv()
model = ChatOpenAI(temperature = 0.5)


message = [("system","You are a comedian who tells a joke about {topic}"),
           ("human","Tell me {joke_count} jokes")]

prompt = ChatPromptTemplate.from_messages(message)

#chain = prompt | model --> The output after invoking this chain has content, metadata, id etc
# if we want to show user just the usefull output then we can use StrOutputParser
chain = prompt | model | StrOutputParser()
print(f'Chain - \n {chain}')

result = chain.invoke({"topic": "Cricketers","joke_count":"2"})

print(f"Result - \n {result}")

