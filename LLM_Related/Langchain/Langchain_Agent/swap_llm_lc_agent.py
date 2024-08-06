# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 12:48:34 2024

@author: snandanw

Description : This is for creating the flow for the Agents, through Langchain. This very basic use of  Langchain Agent Tavily.
Reference - Langchain Oficial Site (https://python.langchain.com/v0.1/docs/integrations/tools/tavily_search/)
"""
# We are gonna use Tavily Search where Tavily's Search API is a search engine built specifically for AI agents (LLMs), delivering real-time, accurate, and factual results at speed.

import getpass
import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI


load_dotenv()


os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")


tool = TavilySearchResults()

#tool.invoke({"query": "What happened in the latest Men T20 WC for India"})
instructions = """You are an assistant"""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

llm = ChatOpenAI(temperature=0)

tavily_tool = TavilySearchResults()
tools =[tavily_tool]
agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               verbose=True)

#agent_executor.invoke({"input": "What happened in the Indian Elections 2024?"})
agent_executor.invoke({"input": "What is the tally of medals for USA in Paris olampics 2024?"})