# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 17:34:23 2024

@author: snandanwar
More on chain, with parellel branching
"""

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

model =  ChatOpenAI(temperature = 0.5)

prompt_template = ChatPromptTemplate.from_messages([("system", "You are an Expert Product reviewer"),
                                      ("human","List the main feature of the Product {product}"),])

# Now we need to creat parellel pipeline where firstly we will get the features of the input and then create parellel brances to get pros and cons from the response recieved.
# Lets write a function to check the Pros of Product
def analyse_pros(features):
    
    pros_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an Expert Product reviewer"),
            ("human","List the Pros from the content {features}")
        ])
    
    return pros_template.format_prompt(features = features).to_string()

# Let's now write a function to check Cons of Product

def analyse_cons(features):
    
    cons_template = ChatPromptTemplate.from_messages([("system", "You are an Expert Product reviewer"),
                                          ("human","List the Cons from the content {features}")])
    
    return cons_template.format_prompt(features = features).to_string()

# We can finally combine this both results as review

def combine_pros_cons(pros,cons):
    return f"Pros:\n {pros}\n\nCons:\n{cons}"

pros_branch = (
    RunnableLambda(lambda x: analyse_pros(x) | model | StrOutputParser())
    )

cons_branch = (
    RunnableLambda(lambda x: analyse_cons(x) | model | StrOutputParser())
    )    
    
chain = (
    prompt_template 
    | model 
    | StrOutputParser() 
    | RunnableParallel(branches={"pros":pros_branch,"cons":cons_branch})
    | RunnableLambda(lambda x:combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"]))
)
#print(f"Chain -\n {chain}")
result = chain.invoke({"product":"iPhone 13 pro"})
print(result)


# Error in this code. Yet to correct it.