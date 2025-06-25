# pylint: skip-file
from langchain_openai import ChatOpenAI,OpenAI
from langchain.prompts import PromptTemplate,ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

def main_template():
    
    template = '''
    Você é um analista financeiro.
    Escreva um relatório financeiro detalhado para a empresa "{empresa}" para o período {periodo}.

    O relatório deve ser escrito em {idioma} e incluir as seguintes análises:
    {analises}

    Certifique-se de fornecer insights e conclusões para cada seção.
    '''
    
    prompt_template = PromptTemplate.from_template(template=template)
    
    empresa = 'ACME Corp'
    periodo = 'Q1 2024'
    idioma = 'Português'
    analises = [
        "Análise do Balanço Patrimonial",
        "Análise do Fluxo de Caixa",
        "Análise de Tendências",
        "Análise de Receita e Lucro",
        "Análise de Posição de Mercado"
    ]
    analises_text = "\n".join([f"- {analise}" for analise in analises])
    print(analises_text)


    prompt = prompt_template.format(
        empresa=empresa,
        periodo=periodo,
        idioma=idioma,
        analises=analises_text
    )
    print("Prompt Gerado:\n", prompt)

    openai = OpenAI(model_name='gpt-3.5-turbo-instruct',max_tokens=1000) #max 4096

    response = openai.invoke(prompt)
    print("Saída do LLM:\n", response)

def main_chat_template():
    #equivalência aos roles: system: system, Human: user, AI: assistant
    chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content='Você deve estruturar suas respostas de acordo com o método de análise de negócios, garantindo clareza e concisão.'),
        HumanMessagePromptTemplate.from_template('Por favor, gere um relatório detalhado sobre a indústria de tecnologia na região "{regiao}".'),
        AIMessage(content='Claro, vou começar coletando informações sobre a região e analisando os dados disponíveis.'),
        HumanMessage(content='Certifique-se de incluir uma análise SWOT e uma previsão de crescimento para os próximos 5 anos.'),
        AIMessage(content='Entendido. Aqui está o relatório completo:')
    ]
    )
    
    prompt_gerado = chat_template.format_messages(regiao='América Latina')
    print(prompt_gerado) 
    
    openai = ChatOpenAI(model_name='gpt-3.5-turbo')
    response = openai.invoke(prompt_gerado) 
    print("Saída do LLM:\n", response.content)
    
if __name__ == "__main__":
    #main_template()
    main_chat_template