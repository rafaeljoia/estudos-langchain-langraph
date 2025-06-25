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



def main():
    try:
        # Inicializa o cliente OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
              
          
        # Faz a requisição para a API
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="Crie uma canção contendo apenas uma estrofe.",
            max_tokens=150,  # Limite de tokens para a resposta
            temperature=0.7  # Controla a criatividade da resposta
        )
        
        # Exibe a resposta completa (para debug)
        print("Resposta completa da API:")
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Extrai e exibe apenas o texto gerado
        message = response.choices[0].text.strip()
        print("Canção gerada:")
        print(message)
        
    except Exception as e:
        print(f"Erro ao fazer requisição para a API: {e}")

if __name__ == "__main__":
    main()