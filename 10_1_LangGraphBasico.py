# pylint: skip-file

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from typing import TypedDict


class State(TypedDict):
    message: str  


def start_node(state):
    print("Início do processo")
    return {"message": "Vamos começar!"}  

def process_node(state):
    print("Processando:", state["message"])  
    return {"message": state["message"] + " Agora estamos processando."} 

def end_node(state):
    print("Finalizando:", state["message"])
    return state


def main():
    # Criando o grafo de estados
    print("Criando o grafo de estados...")
    graph = StateGraph(State)  
    graph.add_node("start", RunnableLambda(start_node))  
    graph.add_node("process", RunnableLambda(process_node))
    graph.add_node("end", RunnableLambda(end_node))
    
    # Transições entre os estados
    print("Adicionando transições entre os estados...")
    graph.set_entry_point("start")
    graph.add_edge("start", "process")
    graph.add_edge("process", "end")
    graph.set_finish_point("end")
    
    executable = graph.compile()
    # Executando
    final_state = executable.invoke({})
    print("\nEstado final:", final_state)

if __name__ == "__main__":
    main()