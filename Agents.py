# pylint: skip-file
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType, Tool

from langchain.prompts import PromptTemplate
import pandas as pd
import yaml
import os

openai = OpenAI(model_name='gpt-4o-mini', temperature=0)

def main_agent():
    # Initialize DuckDuckGoSearchRun properly
    ddg_search = DuckDuckGoSearchRun()
    
    # Create a proper Tool object for the search function
    search_tool = Tool(
        name="DuckDuckGo Search",
        description="Search the web for current information",
        func=ddg_search.run
    )
    
    # Create a list of tools
    tools = [search_tool]
    
    # Initialize agent with tools (not create_python_agent)
    agent = initialize_agent(
        tools=tools,
        llm=openai,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Define the query
    query = "INATEL Santa Rita do Sapucaí-MG"
    
    # Create the prompt
    prompt = f"Pesquise na web sobre {query} e forneça um resumo abrangente sobre o assunto."
    print(f"Prompt: {prompt}\n")
    
    # Execute the agent
    try:
        response = agent.run(prompt)
        print("Resposta do agente:")
        print(response)
    except Exception as e:
        print(f"Erro ao executar o agente: {e}")

if __name__ == "__main__":
    main_agent()