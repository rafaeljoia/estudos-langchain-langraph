# pylint: skip-file

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

openai = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=0)

def simple_chain():
    prompt_template = PromptTemplate.from_template("Descreva as tendências tecnológicas em {ano} em 50 caracteres.")
    runnable_sequence = prompt_template | openai
    output = runnable_sequence.invoke({"ano": "2025"})
    
    print("Output:\n", output)

if __name__ == "__main__":
    simple_chain()