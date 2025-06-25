# pylint: skip-file
from langchain_openai import OpenAI, ChatOpenAI
import os

def main_openAI():
         
    #Uso básico do Langchain com OpenAI
    openai = OpenAI(model_name='gpt-3.5-turbo-instruct')
    frequency_penalty=1
    presence_penalty = 1
    temperature =  1
    max_tokens=50
    n = 1
    seed = 123
    
    response = openai.invoke(input='Quem foi Carl Sagan?', temperature=temperature,
                        frequency_penalty=frequency_penalty,presence_penalty=presence_penalty,
                        max_tokens=max_tokens,n=n, seed=seed)
    print(response)
        


def main_chat_openAI():
    # Uso básico do Langchain com OpenAI Chat 
    
    openai = ChatOpenAI(model_name='gpt-3.5-turbo')
    messages = [
        {"role": "system", "content": "Você é um assistente que fornece informações sobre figuras históricas."},
        {"role": "user", "content": "Quem foi Carl Sagan?"}
    ]
    response = openai.invoke(messages)
    print(response)


if __name__ == "__main__":
    #main_openAI()
    main_chat_openAI()