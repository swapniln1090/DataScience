# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 17:31:26 2024

@author: snandanw
Prompt Tamplete explaination
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(temperature = 0.5)

# creating a Prompt

template = "Tell me a Joke about {topic}"

prompt_template = ChatPromptTemplate.from_template(template)

print(f'{prompt_template}')

prompt = prompt_template.invoke({"topic":"cats"})

result = model.invoke(prompt)
print(result.content)
print("\n")

# Let's place multiple placeholders

template = """ You are a Doctor and help with query as.
Human: Tell me the symptoms of {decease} and tell me medicine for age {ages}.
Assistant:
"""

prompt_multiple = ChatPromptTemplate.from_template(template)
print(f"Prompt 1 - {prompt_multiple}") 
prompt = prompt_multiple.invoke({"decease":"Malaria","ages":"40"})
##prompt = prompt_multiple.invoke({"decease":"Large Language Modele","ages":"40"})

print(f"Prompt 2 - {prompt}")
result = model.invoke(prompt)
print(result.content)


# Prompt with System and Human Messages
print(f"---------Prompt with System and Human Message (Tuple)--------------\n")
message = [("system","You are a comedian who tells Joke about {topic}"),
           ("human","Tell me {joke_count} jokes")]

prompt_template = ChatPromptTemplate.from_messages(message)
print(prompt_template)
prompt = prompt_template.invoke({"topic":"Doctors","joke_count":"2"})
print(prompt)
result = model.invoke(prompt)
print(result.content)