# pylint: skip-file
"""
Sistema RAG (Retrieval Augmented Generation) para análise de documentos jurídicos
"""

import os
import zipfile
import logging
from typing import List
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain_community.vectorstores.pinecone import Pinecone as LangchainPinecone
from langchain_community.vectorstores import Pinecone as PineconeVectorStore

from pinecone import Pinecone  # novo SDK
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()
INDEX_NAME = 'llm'
from pinecone import Pinecone, ServerlessSpec

class DocumentProcessor:
    def __init__(self):
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.pinecone_environment = os.getenv('PINECONE_ENVIRONMENT')
        self.pinecone_region = os.getenv('PINECONE_REGION') or "us-east-1"  # padrão se não estiver definido
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.index_name = os.getenv('PINECONE_INDEX_NAME') or 'llm'

        if not self.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY não encontrada.")
        if not self.pinecone_environment:
            raise ValueError("PINECONE_ENVIRONMENT não encontrada.")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não encontrada.")
        
        # Inicializa cliente Pinecone usando a nova API
        self.pinecone = Pinecone(api_key=self.pinecone_api_key)

        self.llm = ChatOpenAI(api_key=self.openai_api_key, model='gpt-3.5-turbo', temperature=0.2)
        self.embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
        
    def extract_zip(self, zip_path: str, extract_path: str) -> bool:
        try:
            if not Path(zip_path).exists():
                logger.error(f"Arquivo ZIP não encontrado: {zip_path}")
                return False

            Path(extract_path).mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if member.startswith('/') or '..' in member:
                        logger.warning(f"Arquivo suspeito ignorado: {member}")
                        continue
                zip_ref.extractall(extract_path)

            logger.info(f"Arquivos extraídos com sucesso para: {extract_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao extrair ZIP: {e}")
            return False

    def load_pdf_documents(self, folder_path: str) -> List[Document]:
        documents = []
        pdf_files = list(Path(folder_path).glob("*.pdf"))

        if not pdf_files:
            logger.warning(f"Nenhum arquivo PDF encontrado em: {folder_path}")
            return documents

        logger.info(f"Encontrados {len(pdf_files)} arquivos PDF")

        for pdf_file in pdf_files:
            try:
                logger.info(f"Processando: {pdf_file.name}")
                loader = PyMuPDFLoader(str(pdf_file))
                docs = loader.load()
                for doc in docs:
                    doc.metadata['source_file'] = pdf_file.name
                    doc.metadata['file_path'] = str(pdf_file)
                documents.extend(docs)
            except Exception as e:
                logger.error(f"Erro ao carregar {pdf_file.name}: {e}")
                continue

        logger.info(f"Total de {len(documents)} páginas carregadas")
        return documents

    def create_chunks(self, documents: List[Document]) -> List[Document]:
        if not documents:
            logger.warning("Nenhum documento para processar")
            return []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

        chunks = text_splitter.split_documents(documents)
        logger.info(f"Criados {len(chunks)} chunks")
        return chunks

    def create_vector_store(self, chunks: List[Document], index_name: str) -> PineconeVectorStore:
        try:
            index_names = self.pinecone.list_indexes().names()
            logger.info(f"Índices disponíveis: {index_names}")
            logger.info(f"Usando índice: {index_name}")

            if index_name not in index_names:
                raise ValueError(f"Índice '{index_name}' não encontrado no Pinecone. Crie-o primeiro.")

            # Passa apenas o nome do índice — LangChain já se conecta automaticamente com `pinecone` instanciado
            vector_store = PineconeVectorStore.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                index_name = 'llm'
                )

            logger.info("Vector store criado com sucesso")
            return vector_store

        except Exception as e:
            logger.error(f"Erro ao criar vector store: {e}")
            raise

    def create_qa_chain(self, vector_store):
        retriever = vector_store.as_retriever(
            search_type='similarity',
            search_kwargs={'k': 5}
        )

        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type='stuff',
            retriever=retriever,
            return_source_documents=True,
            verbose=True
        )

        return chain

def main():
    try:
        ZIP_FILE = 'documentos.zip'
        EXTRACT_FOLDER = 'docs'
        INDEX_NAME = 'llm'

        processor = DocumentProcessor()

        logger.info("=== Extraindo arquivos ===")
        if not processor.extract_zip(ZIP_FILE, EXTRACT_FOLDER):
            logger.error("Falha na extração dos arquivos")
            return

        logger.info("=== Carregando documentos PDF ===")
        documents = processor.load_pdf_documents(EXTRACT_FOLDER)
        if not documents:
            logger.error("Nenhum documento carregado")
            return

        logger.info("=== Criando chunks ===")
        chunks = processor.create_chunks(documents)
        if not chunks:
            logger.error("Nenhum chunk criado")
            return

        logger.info("=== Criando vector store ===")
        vector_store = processor.create_vector_store(chunks, INDEX_NAME)

        logger.info("=== Criando cadeia QA ===")
        qa_chain = processor.create_qa_chain(vector_store)

        queries = [
            "Responda apenas com base no input fornecido. Qual o número do processo que trata de Violação de normas ambientais pela Empresa de Construção?",
            "Responda apenas com base no input fornecido. Qual foi a decisão no caso de fraude financeira?",
            "Responda apenas com base no input fornecido. Quais foram as alegações no caso de negligência médica?",
            "Responda apenas com base no input fornecido. Quais foram as alegações no caso de Número do Processo: 822162"
        ]

        logger.info("=== Executando perguntas ===")
        for i, query in enumerate(queries, 1):
            try:
                print(f"\n{'='*60}")
                print(f"PERGUNTA {i}:")
                print(f"{'='*60}")
                print(query)
                print(f"{'-'*60}")

                result = qa_chain.invoke(query)

                print("RESPOSTA:")
                print(result['result'])

                if 'source_documents' in result and result['source_documents']:
                    print(f"\nFONTES ({len(result['source_documents'])} documentos):")
                    for j, doc in enumerate(result['source_documents'][:3], 1):
                        source = doc.metadata.get('source_file', 'Desconhecido')
                        print(f"  {j}. {source}")

            except Exception as e:
                logger.error(f"Erro ao processar pergunta {i}: {e}")
                continue

        logger.info("=== Processamento concluído ===")

    except Exception as e:
        logger.error(f"Erro na função principal: {e}")
        raise

if __name__ == "__main__":
    main()
