# pylint: skip-file
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun,WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def main_REPL():
    python_repl = PythonREPL()
    result = python_repl.run("print(5 * 5)")
    print(result)
    
def main_search():
    search_tool = DuckDuckGoSearchRun()
    result = search_tool.run("Santa Rita do Sapucaí-MG", {"max_results": 1})
    print(result)
    
def main_wikipedia():
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    result = wikipedia_tool.run("Minas Gerais")
    print(result)
    


if __name__ == "__main__":  
    main_search()