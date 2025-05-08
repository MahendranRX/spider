from langchain_pinecone import PineconeVectorStore
from langchain_community.llms.cohere import Cohere
from store_data import get_embeddings
# import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()

# GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

# genai.configure(api_key=GEMINI_API_KEY)


def get_answer(question):

    index_name = 'spider'

    embeddings = get_embeddings()

    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name, embedding=embeddings
    )

    retriever = docsearch.as_retriever(search_type='similarity',
                                       search_kwargs={'k': 3})

    # llm = genai.GenerativeModel(model_name='gemini-1.5-pro')

    llm = Cohere(cohere_api_key=COHERE_API_KEY, model="command-r-plus",)

    retrieved_documents = retriever.invoke(question)

    documents_text = '\n'.join(
        [doc.page_content for doc in retrieved_documents])

    prompt = [f"""
        User:
        You are a highly experienced assistant specializing in Swiss tax submission.
        Your task is to answer questions **strictly based on the provided DOCUMENTS** while maintaining accuracy and clarity.

        ### **Response Format:**
        - List key points in **bullet points**, ensuring each point appears on a **new line**.
        - Format each point **clearly and concisely**:
            - **First key point**
            - **Second key point**
            - **Additional points if necessary**

        ### **Important Guidelines:**
        1. **Only use information from the DOCUMENTS.**
        - If the answer is not found in the DOCUMENTS, respond with:
            **"Sorry, I don't know."**
        2. **Stay within the scope of the question.**
        - **Avoid assumptions** or external information.
        3. **Failure to follow these rules may result in losing your role.**

        ---
        ### **Question:**
        {question}

        ### **DOCUMENTS:**
        {documents_text}
        ---

        **Assistant:**
        """]

    response = llm.generate(prompts=prompt)

    print(response.generations)
    return response.generations[0][0].text.strip()
