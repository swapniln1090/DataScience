# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 20:05:16 2024

@author: snandanw
Description - This code is more advanced version on LLM Agents through Langchain. I have also added few more descriptions below for better understanding
"""

import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_tool_calling_agent

from langchain_core.messages import AIMessage, HumanMessage
#For memory 
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()


os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")


# Tavily
search = TavilySearchResults()

#search.invoke("what is the weather in Birmingham, AL")

# Retriver (as we do in RAG pipeline where we store document's text in Vector Database in an Embedding form.)

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)

vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()


#retriever.invoke("how to upload a dataset")[0]

# So above we have seen that we have made use of Tavily and Vectordatabase( for RAG).
# Now that we have populated our index that we will do doing retrieval over, we can easily turn it into a tool (the format needed for an agent to properly use it)

retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)


# Tools - After creating Tavily Search and Retriver tool we need to create "list" of tool that can be used downstream.
tools = [search, retriever_tool]


### Creating an Agent

"""Now that we have defined the tools, we can create the agent. 
We will be using an OpenAI Functions agent - for more information on this type of agent.
Reference to types of Agents - https://python.langchain.com/v0.1/docs/modules/agents/agent_types/  """

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

# Next, we choose the prompt we want to use, to guide the agent.
# Ref - https://smith.langchain.com/hub/hwchase17/openai-functions-agent

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")
prompt.messages

"""Now, we can initialize the agent with the LLM, the prompt, and the tools. 
The agent is responsible for taking in input and deciding what actions to take. 
Crucially, the Agent does not execute those actions - that is done by the AgentExecutor.
Reference - https://api.python.langchain.com/en/latest/agents/langchain.agents.tool_calling_agent.base.create_tool_calling_agent.html"""

agent = create_tool_calling_agent(llm, tools, prompt)

#Finally, we combine the agent (the brains) with the tools inside the AgentExecutor (which will repeatedly call the agent and execute tools).

agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)


# Run the agent
#agent_executer.invoke({"input":"Hi! How are you"})
#agent_executer.invoke({"input": "how can langsmith help with testing?"})
# agent_executer.invoke({"input": "whats the weather in sf?"})
# If I ask anything related to my previous questions I would not get the proper result because it does not hold past history in its memory. 
# Example - agent_executer.invoke({"input": "whats did i ask about sf earlier?"}) 
# output is -
"""{'input': 'whats did i ask about sf earlier?',
 'output': 'I couldn\'t find the specific question you asked about "sf" earlier. If you can provide more context or details, I\'ll be happy to assist you further.'}"""

# Adding in memory

"""
As mentioned earlier, this agent is stateless. This means it does not remember previous interactions. 
To give it memory we need to pass in previous chat_history. Note: it needs to be called chat_history because of the prompt we are using. 
If we use a different prompt, we could change the variable name
"""

# Here we pass in an empty list of messages for chat_history because it is the first message in the chat
memory = ChatMessageHistory(session_id="test-session")

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executer,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

agent_with_chat_history.invoke(
    {"input": "What is the Population of India"},
    config={"configurable": {"session_id": "<foo>"}},
)

#To test the memory of this agent, we can ask a followup question that relies on information in the previous exchange to be answered correctly.
agent_with_chat_history.invoke(
    {"input": "what is their national animal called?"},
    config={"configurable": {"session_id": "<foo>"}},
)

agent_with_chat_history.invoke(
    {"input": "what is their Criket Team captian name?"},
    config={"configurable": {"session_id": "<foo>"}},
)
