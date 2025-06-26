# 🦜🔗 LangChain & LangGraph - Estudos

## 🎯 Sobre o Projeto

Este repositório contém exemplos práticos e implementações usando **LangChain** e **LangGraph** obtidos nos estudos do curso do prof. Fernado Amaral - Udemy.


### O que você encontrará aqui:
- 🤖 Agentes 
- 📚 Sistemas RAG para análise de documentos
- 🔍 Ferramentas de busca e pesquisa
- 🌐 Integração com APIs externas

## 🚀 Instalação

### Pré-requisitos
- Python 3.11
- pip ou conda

### Instalação Completa
```bash

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
projeto/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── agents/
│   │   ├── search_agent.py
│   │   └── qa_agent.py
│   ├── chains/
│   │   ├── rag_chain.py
│   │   └── summary_chain.py
│   ├── graphs/
│   │   ├── workflow_graph.py
│   │   └── decision_graph.py
│   ├── tools/
│   │   ├── web_search.py
│   │   └── document_loader.py
│   └── utils/
│       ├── config.py
│       └── helpers.py
├── examples/
│   ├── basic_chatbot.py
│   ├── rag_system.py
│   └── agent_workflow.py
├── data/
│   ├── documents/
│   └── embeddings/
└── tests/
    ├── test_agents.py
    └── test_chains.py
```

## ⚙️ Configuração

### 1. Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:

```env
# APIs
OPENAI_API_KEY=sua_chave_openai_aqui
PINECONE_API_KEY=sua_chave_pinecone_aqui
PINECONE_ENVIRONMENT=sua_região_pinecone

# Configurações
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=sua_chave_langsmith_opcional
```

## 📚 Recursos Adicionais

### Documentação Oficial
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

### Tutoriais e Guias
- [LangChain QuickStart](https://python.langchain.com/docs/get_started/quickstart)
- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Agents Tutorial](https://python.langchain.com/docs/modules/agents/)

### Comunidade
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [Discord LangChain](https://discord.gg/langchain)
- [Twitter @LangChainAI](https://twitter.com/langchainai)

### Cursos e Certificações
- [DeepLearning.AI - LangChain Course](https://www.deeplearning.ai/)
- [Coursera - LLM Applications](https://www.coursera.org/)

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Time do LangChain pela framework incrível
- Comunidade open source
- Contribuidores do projeto

---
