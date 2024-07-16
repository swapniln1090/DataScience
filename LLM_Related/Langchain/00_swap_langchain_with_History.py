# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 00:56:13 2024

@author: snandanw

MOre on Langchain
"""

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(temperature = 0.6) ## By default withrispect to key, it has taken gpt-3.5-turbo. But its good to specify explicitly for better readability.
#result = model.invoke("What is 50 divide by 4?")
#print(result)

chat_history = []

system_msg = SystemMessage(content = "You act like Helpful Assistant")
chat_history.append(system_msg)

while True:
    query = input("You : ")
    if query.lower()=="exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = model.invoke(input = chat_history)
    response = result.content
    chat_history.append(response)
    
    print(f"AI Resonse : {response}")
    
print("--------------Chat History-------------")
print(chat_history)
