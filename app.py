import streamlit as st
from store_data import upload_data_from_pdf
from get_answer import get_answer


def main():

    with st.sidebar:
        pdf_files = st.file_uploader(
            '**Upload Your Pdf and chat**', accept_multiple_files=True)

        if pdf_files:
            with st.spinner('Your Pdfs are Processing'):
                upload_data_from_pdf(pdf_files)
                st.success('Your pdfs are processed successfully')

    st.title("Chat with your own data")

    instruction = """
    This AI-powered chatbot designed for answering the Switzerland Tax related questions. So you can ask 
    the questions like,

        1. what are the taxes in swiss
        2. what is wealth tax
        3. what is value added tax,  etc.

    """
    st.markdown(instruction)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    question = st.chat_input(
        placeholder="Ask me with Swiss tax related Question")

    if question:
        st.session_state.conversation.append(
            {'role': 'user', 'content': question})

        with st.spinner('Processing'):
            response = get_answer(question)

            st.session_state.conversation.append(
                {'role': 'assistant', 'content': response})

        for message in st.session_state.conversation:
            with st.chat_message(message['role']):
                st.markdown(message['content'])


if __name__ == '__main__':
    main()
