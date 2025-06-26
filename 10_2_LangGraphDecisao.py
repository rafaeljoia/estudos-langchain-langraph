# pylint: skip-file

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from duckduckgo_search import DDGS
from typing import TypedDict
import graphviz


llm = ChatOpenAI(model_name="gpt-4.1", temperature=0.3)


class State(TypedDict):
    pergunta: str  
    conteudo: str 
    resposta: str 
    

def recebe_pergunta(state: State) -> State:
    print(f"Usuário perguntou: {state['pergunta']}")
    return {"pergunta": state["pergunta"]}

def precisa_pesquisar(state: State) -> State:
    pergunta = state["pergunta"].lower()
    precisa = any(p in pergunta for p in ["dados", "estatísticas", "números", "pesquisa"])
    print("Precisa pesquisar?", precisa)
    # Retorna um dicionário, com chave especial para decisão
    return {"next_step": "pesquisar" if precisa else "consultar_llm"}

def pesquisar(state: State) -> State:
    pergunta = state["pergunta"]
    print(f"Pesquisando no DuckDuckGo: {pergunta}")

    with DDGS() as ddgs:
        resultados = ddgs.text(pergunta, max_results=1)

    if resultados:
        contexto = "\n".join([r["body"] for r in resultados if "body" in r])
    else:
        contexto = "Nenhum resultado encontrado."

    return {"conteudo": contexto}    

def consultar_llm(state: State) -> State:
    prompt = ChatPromptTemplate.from_template("Responda à seguinte pergunta: {pergunta}")
    chain = prompt | llm
    resposta = chain.invoke({"pergunta": state["pergunta"]})
    print("Resposta direta do LLM.")
    return {"resposta": resposta.content}

def sintetizar(state: State) -> State:
    contexto = state.get("conteudo", "")
    pergunta = state["pergunta"]
    prompt = ChatPromptTemplate.from_template("""
    Use o seguinte contexto para responder a pergunta:
    Contexto: {contexto}
    Pergunta: {pergunta}
    Resposta:""")
    chain = prompt | llm
    resposta = chain.invoke({"contexto": contexto, "pergunta": pergunta})
    print("Resposta sintetizada com contexto.")
    return {"resposta": resposta.content}

def responder(state: State) -> State:
    print("\n Resposta Final:")
    print(state["resposta"])
    return state


def main():
    
    graph = StateGraph(State)

    graph.add_node("recebe_pergunta", RunnableLambda(recebe_pergunta))
    graph.add_node("decisao", RunnableLambda(precisa_pesquisar))
    graph.add_node("pesquisar", RunnableLambda(pesquisar))
    graph.add_node("consultar_llm", RunnableLambda(consultar_llm))
    graph.add_node("sintetizar", RunnableLambda(sintetizar))
    graph.add_node("responder", RunnableLambda(responder))
    
    
    graph.set_entry_point("recebe_pergunta")

    graph.add_edge("recebe_pergunta", "decisao")
    graph.add_conditional_edges(
    "decisao",
    lambda state: state["next_step"],  
    {
        "pesquisar": "pesquisar",
        "consultar_llm": "consultar_llm"
    }
    )
    graph.add_edge("pesquisar", "sintetizar")
    graph.add_edge("consultar_llm", "responder")
    graph.add_edge("sintetizar", "responder")
    graph.set_finish_point("responder")
    
    
    executable = graph.compile()

    print("\n TESTE 1:")
    executable.invoke({"pergunta": "Qual é a capital da Alemanha?"})

    print("\n  TESTE 2:")
    executable.invoke({"pergunta": "Me mostre dados sobre economia brasileira em 2025."})
    
    #Geração memaid graph 
    dot = executable.get_graph().draw_mermaid()
    print("\n Diagrama do grafo:")
    print(dot)  
    
    
if __name__ == "__main__":
    main()
    