from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')


def scrap_from_pdf(pdf_files):
    directory = Path('data')

    if not directory.exists():
        directory.mkdir()

    for pdf in pdf_files:
        with open(os.path.join(directory, pdf.name), 'wb') as file:
            file.write(pdf.getbuffer())

    loader = PyPDFDirectoryLoader(directory, glob='*.pdf')

    data = loader.load()

    for file in directory.iterdir():
        file.unlink()
    directory.rmdir()

    return data


def split_text(data):
    text_splitter = RecursiveCharacterTextSplitter(
        separators='\n', chunk_size=1000, chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_documents(data)

    text_chunks = []

    for chunk in chunks:
        text = str(chunk).replace('\n', ' ')
        text.replace('\t', ' ').strip()
        text_chunks.append(Document(text))

    return text_chunks


def get_embeddings():
    embeddings = CohereEmbeddings(model='embed-english-v3.0',
                                  user_agent='spider')
    return embeddings


def upload_data(chunks):
    pc = Pinecone(api_key=PINECONE_API_KEY)

    embeddings = get_embeddings()

    index_name = 'spider'

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )

    PineconeVectorStore.from_documents(
        documents=chunks, embedding=embeddings,
        index_name=index_name
    )


def upload_data_from_pdf(pdf_files):
    data = scrap_from_pdf(pdf_files)
    chunks = split_text(data)
    upload_data(chunks)
