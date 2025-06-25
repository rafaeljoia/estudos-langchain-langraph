# pylint: skip-file
import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Verifica se a API key foi carregada
if 'OPENAI_API_KEY' not in os.environ:
    print("Erro: OPENAI_API_KEY não encontrada no arquivo .env")
    print("Certifique-se de que o arquivo .env contém: OPENAI_API_KEY=sua_chave_aqui")
    exit(1)

model = 'gpt-3.5-turbo'

def main():
    try:
        # Inicializa o cliente OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        """     
        # Faz a requisição para a API
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Conte uma Piada!"}]
        )
        
        # Exibe a resposta completa (para debug)
        print("Resposta completa da API:")
        print(response)
        print(type(response))
        
        message = (response.choices[0].message.content)
        print(message)
         """
        """ print("Outras Roles")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a fictional investment assistant."},
                {"role": "user", "content": "What is the best low-risk investment you recommend for this year?"}
            ]
            )
        
        print("Resposta da API:")
        message = (response.choices[0].message.content)
        print(message) """
        
        # Assistant message
        """    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "assistant", "content": message},
            {"role": "user", "content": "What are the risks related to Government bonds?"}
        ]
        ) """
        
        #Hiper Parameters
        # frequency_penalty=1 é usado para reduzir a repetição de palavras.
        # presence_penalty=1 é usado para incentivar a inclusão de novas palavras.
        # temperature=1 é usado para aumentar a aleatoriedade e criatividade da resposta.
        # max_tokens=100 limita o tamanho da resposta a 100 tokens.  
        # n=2 gera duas respostas diferentes.
        # seed=123 é usado para garantir a reprodutibilidade da resposta.
        # stop=["shadows","mortal "] define palavras que, se encontradas, interrompem a geração de texto.   
        
        response = client.chat.completions.create(
            model=model,
            frequency_penalty=1,
            presence_penalty = 1,
            temperature =  1 ,
            max_tokens=50,
            n = 1 ,
            seed = 123,
            #stop = ["shadows","mortal "],
            messages=[
                {"role": "system", "content": "You are a depressed and disillusioned poet."},
                {"role": "user", "content": "Compose a poem about the ephemerality of existence."}
            ]
        )
        
        message = (response.choices[0].message.content)
        print(message)
                    
    except Exception as e:
        print(f"Erro ao fazer requisição para a API: {e}")

if __name__ == "__main__":
    main()