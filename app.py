import streamlit as st
from store_data import upload_data_from_pdf

def main():

    with st.sidebar:
        pdf_files = st.file_uploader('**Upload Your Pdf**', accept_multiple_files=True)

        if pdf_files:
            with st.spinner('Your Pdfs are Processing'):
                upload_data_from_pdf(pdf_files)
                st.success('Your pdfs are processed successfully')

    st.title("Chat with your own data")

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    question = st.chat_input(placeholder="Ask me with Swiss tax related Question")



if __name__ == '__main__':
    main()