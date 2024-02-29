import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter




load_dotenv()
st.set_page_config(page_title="Chat with your own report", page_icon=":books:")

def get_pdf_text(file_uploaded):
    text = ""
    for pdf in file_uploaded:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# def get_keywords(pdf_doc):
#     reader = PdfReader(pdf_doc)
#     #keywords=[]
#     for page in reader.pages:
#         text = page.extract_text()
#         tokens = nltk.word_tokenize(text)
#         stop_words = set(stopwords.words('english'))
#         filtered_text = [word for word in tokens if not word.lower() in stop_words]
#         keywords = [word.lower() for word in filtered_text if word.isalpha()]        
    # return keywords
class ReportKeywords:
    def __init__(self):
        self.keywords = {}

    def add_keyword(self, keyword, definition):
        self.keywords[keyword] = definition

    def get_definition(self, keyword):
        return self.keywords.get(keyword, "Definition not found.")
        


class ReportKeywords:
    def __init__(self):
        self.keywords = {}

    def add_keyword(self, keyword, definition):
        self.keywords[keyword] = definition

    def get_definition(self, keyword):
        return self.keywords.get(keyword, "Definition not found.")
    



def main():

    report_keywords = ReportKeywords()

    report_keywords.add_keyword("Keyword1", "Definition1")
    report_keywords.add_keyword("Keyword2", "Definition2")

    st.header("Your report's key definitions :heavy_exclamation_mark:")
    for keyword, definition in report_keywords.keywords.items():
        st.write(f"**{keyword}:** {definition}")

    with st.sidebar:
        st.subheader("Your Report")
        file_uploaded = st.file_uploader("Upload your report here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):

                # get pdf text
                raw_text = get_pdf_text(file_uploaded)
                # st.write(raw_text)  

                # getting text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)    

                #keywords
                # key_words=get_keywords(file_uploaded)
                # for word in key_words:
                #     report_keywords.add_keyword(word, "Definition1")
                # for keyword, definition in report_keywords.keywords.items():
                #     st.write(f"{keyword}: {definition}")       

    st.header("Chat with your own report :page_with_curl:")

    previous_messages = st.session_state.get("previous_messages", [])

    for message in previous_messages:
        # st.markdown(f'<div class="message-bubble">{message}</div>', unsafe_allow_html=True)
        if message.startswith("User:"):
            st.markdown(f'<div class="message-bubble user" style="color: black;">{message}</div>', unsafe_allow_html=True)
        elif message.startswith("ChatDoc:"): 
            st.markdown(f'<div class="message-bubble gpt" style="color: black;">{message}</div>', unsafe_allow_html=True)

    user_question = st.text_input("Ask a question about your report:")
    if user_question:
        st.session_state.previous_messages.append(f"User: {user_question}")

        answer = get_answer_from_gpt(user_question, report_keywords)

        st.session_state.previous_messages.append(f"ChatDoc: {answer}")
        st.markdown(f'<div class="message-bubble gpt" style="color: black;">{answer}</div>', unsafe_allow_html=True)

def get_answer_from_gpt(question, report_keywords):

    answer = f"Answer for '{question}'"
    return answer

if __name__ == "__main__":
    st.markdown(
        """
        <style>
        .message-container {
            display: flex;
            flex-direction: column-reverse;
        }
        .message-bubble {
            display: inline-block;
            padding: 10px;
            margin: 5px;
            border-radius: 8px;
            background-color: #123499;  /* Adjust the background color as needed */
            color: white;  /* Adjust the font color as needed */
        }
        .user {
            align-self: flex-right;
            float:right;
            background-color: #74AA9C;  /* Adjust the background color as needed */
        }
        .gpt {
            align-self: flex-start;
            background-color: #74AA9C;  /* Adjust the background color as needed */
            
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if "previous_messages" not in st.session_state:
        st.session_state.previous_messages = []
    main()