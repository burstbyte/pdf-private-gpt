from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from PIL import Image

import openai
# Update this line with your new API key
# new_api_key = "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"

# Set the new API key
# openai.api_key = new_api_key

# Print the API key for verification
print("Using API key:", openai.api_key)

# Now make your OpenAI API requests as usual

def main():
    load_dotenv()
    st.set_page_config(page_title="AI project by FFS")
    st.header("Ask your PDF 💬 - @ffs.ai")


    #opening the image
    image = Image.open('ask-a-book.jpg')

    #displaying the image on streamlit app
    st.image(image, caption='Ask a Book Questions with LangChain and OpenAI')


    # upload file
    pdf = st.file_uploader("Upload your PDF !", type="pdf")

    # extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # show user input
        user_question = st.text_input("Ask a question about your PDF:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
        
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)

            st.write(response)

            st.write(cb)



if __name__ == '__main__':
    main()
