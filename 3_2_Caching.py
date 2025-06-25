# pylint: skip-file

from langchain_openai import OpenAI
from langchain.cache import InMemoryCache,SQLiteCache
from langchain.globals import set_llm_cache
import os
import json
import hashlib

openai = OpenAI(model_name='gpt-3.5-turbo-instruct')

class SimpleDiskCache:
    def __init__(self, cache_dir='cache_dir'):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, key):
        hashed_key = hashlib.md5(key.encode()).hexdigest() #hasg cria nome de arquivo único
        return os.path.join(self.cache_dir, f"{hashed_key}.json")

    def lookup(self, key, llm_string):
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)
        return None

    def update(self, key, value, llm_string):
        cache_path = self._get_cache_path(key)
        with open(cache_path, 'w') as f:
            json.dump(value, f)
    


def cache_memoria():
    
    set_llm_cache(InMemoryCache())

    prompt = 'Me diga em poucas palavras, com 50 caracteres, quem foi Carl Sagan.'
    response1 = openai.invoke(prompt)
    print("Primeira resposta (API chamada):", response1)

    response2 = openai.invoke(prompt)
    print("Segunda resposta (usando cache):", response2)


def cache_disco_dbsqlite():
    
    cache = SQLiteCache(database_path="langchain_cache.db")
    set_llm_cache(cache)
    
    prompt = 'Me diga em poucas palavras, com 50 caracteres, quem foi Neil Armstrong.'
    
    response1 = openai.invoke(prompt)
    print("Primeira resposta (API chamada):", response1)
    
    response2 = openai.invoke(prompt)
    print("Segunda resposta (usando cache):", response2)
    
def cache_personalizado():
    # Cada prompt gera um cache diferente
    
      
    cache = SimpleDiskCache(cache_dir='custom_cache_dir')
    set_llm_cache(cache)
    prompt = 'Me diga em poucas palavras, com 50 caracteres, quem foi Albert Einstein.'
    
    cache_response = cache.lookup(prompt, None)
    if cache_response:
        print("Resposta encontrada no cache:", cache_response)
        return
    reponse = openai.invoke(prompt)
    cache.update(prompt, reponse, None)
    print("Cache atualizado com a resposta:", reponse)

if __name__ == "__main__":
    #cache_memoria()
    #cache_disco_dbsqlite()
    cache_personalizado()