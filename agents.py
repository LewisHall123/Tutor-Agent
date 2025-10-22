"""
Module for setting up three LangChain agents:
1. A question generator for students.
2. A marker for evaluating answers.
3. A progress report updater.

OpenAI API key is loaded from a .env file.
"""

import os
import getpass
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from get_time import get_date
from Load_docs import search_notes, read_file, write_file


# Loads in environment variables from the .env file
load_dotenv()

# Gets API key from .env file
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# Setup for the LLM to be use by the agents
llm = ChatOpenAI(model="gpt-5-mini-2025-08-07",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    )

# First agent: generates 8 questions for the student
agent1 = create_agent(
    model=llm,
    tools = [get_date, read_file, search_notes],
    system_prompt = 
    "You are a teacher. Your initial prompt was a description of the different topics the student is learning." 
    "First task: Use get_date to get the date for today (dd-mm-yyyy)." 
    "Second task: Use read_file to access a progress report of how the student is doing on the different topics." 
    "Third task: Chose two specific topics from the inital prompt of different topics, from the progress report choose"
    "two topics the student has struggled with 5 or more days ago. These four topics are what you will test the student on"
    "Fourth task: Use search_notes to find information regarding these four topics."
    "Fifth task: Using the information you retrieved on those 4 topics, think of two normal questions, and two programming questions," 
    "Structure your output like this:\n"
    "1. Quesion one"
    "2. Question two..."
    "Output just the questions and nothing else"
)

# Second agent: Marks the students answers to the questions
agent2 = create_agent(
    model=llm,
    tools = [search_notes],   
    system_prompt=
    "You are a teacher. You have been given a set of questions and the students answers to those questions" 
    "Always use the search_notes tool to find information regarding the questions and answers"
    "Mark the questions, if any answer was incorrect or there was any small errors, explain them."
)

# Third agent: Updates the students progress report
agent3 = create_agent(
     model=llm,
    tools = [get_date, read_file, write_file],   
    system_prompt=
    "You are a teacher. You have been given an input of questions a student has been asked, the students answers,"
    "and the marking of those questions." 
    "First task: use get_date to find the date for today." 
    "Second task: use read_file to read the progress report of a student."
    "Third task: use write_file to overwrite the content of the progress report to add new information regarding what the student got wrong, remove information" 
    "that no longer holds true if the studnt now understands something he no longer did, and write in the information that did not change. " 
    "Fourth task: respond with a very short sentence confirming you have carried out the instructions and nothing else."
)



'''
agent1 = create_tool_calling_agent(llm, tools, prompt1)

agent_executor1 = AgentExecutor(agent=agent1, tools=tools)

tools = [get_date, search_notes]

prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a teacher. Always use the search_notes tool to find information regarding the students questions,",
        "your questions to the student, and the students answers. Use the get_date to get todays date"),
        ("student", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
'''

# from langchain_core.tools import tool
# from langchain.agents import AgentExecutor, create_tool_calling_agent
# from langchain_core.prompts import ChatPromptTemplate