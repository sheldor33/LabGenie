import os

import nltk
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from PyPDF2 import PdfReader

st.set_page_config(page_title="Chat with LabGenie", page_icon="🧞")


def ensure_nltk_data() -> None:
    """Download NLTK assets once per container/session."""
    for resource in ("punkt", "punkt_tab", "stopwords"):
        try:
            if resource == "stopwords":
                nltk.data.find(f"corpora/{resource}")
            else:
                nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)


def get_openai_api_key() -> str:
    """Prefer Streamlit secrets, fall back to .env / environment."""
    load_dotenv()
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if not key:
            st.error(
                "Missing `OPENAI_API_KEY`. Add it in Streamlit Secrets "
                "or a local `.env` file."
            )
            st.stop()
        return key


@st.cache_resource
def get_chat_model():
    os.environ["OPENAI_API_KEY"] = get_openai_api_key()
    return ChatOpenAI(temperature=0.2)


def get_keywords(pdf_doc) -> list[str]:
    reader = PdfReader(pdf_doc)
    keywords: list[str] = []
    stop_words = set(nltk.corpus.stopwords.words("english"))

    for page in reader.pages:
        text = page.extract_text() or ""
        tokens = nltk.word_tokenize(text)
        filtered = [
            word.lower()
            for word in tokens
            if word.isalpha() and word.lower() not in stop_words
        ]
        keywords.extend(filtered)

    return sorted(set(keywords))


def main() -> None:
    ensure_nltk_data()
    chat = get_chat_model()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            SystemMessage(
                content=(
                    "You're a helpful assistant that describes health-related "
                    "terms briefly, their healthy levels in the body, and tips "
                    "to keep them balanced."
                )
            )
        ]
    if "previous_messages" not in st.session_state:
        st.session_state.previous_messages = []
    if "definition" not in st.session_state:
        st.session_state.definition = ""

    st.header("Your report's key definitions :heavy_exclamation_mark:")

    with st.sidebar:
        st.subheader("Your Report")
        file_uploaded = st.file_uploader(
            "Upload your lab report PDF, then click Process",
            type=["pdf"],
        )
        if st.button("Process"):
            if file_uploaded is None:
                st.warning("Please upload a PDF report first.")
            else:
                with st.spinner("Extracting keywords and generating definitions..."):
                    keywords = get_keywords(file_uploaded)
                    for word in keywords:
                        st.write(word)

                    kw_str = ", ".join(keywords)
                    query = [
                        SystemMessage(
                            content=(
                                "You are a helpful assistant that identifies terms "
                                "directly or indirectly related to proteins, enzymes, "
                                "and hormones found in the body from the list of words "
                                "provided, defines them briefly, mentions healthy levels "
                                "in medical units, and tips to keep them balanced."
                            )
                        ),
                        HumanMessage(content=kw_str),
                    ]
                    st.session_state.definition = chat.invoke(query).content

    if st.session_state.definition:
        st.write(st.session_state.definition)

    st.header("Chat with LabGenie 🧞")
    for message in st.session_state.previous_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("I am your LabGenie. How may I help you?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.previous_messages.append(
            {"role": "user", "content": prompt}
        )
        st.session_state.chat_history.append(HumanMessage(content=prompt))

        ai_response = chat.invoke(st.session_state.chat_history).content
        st.session_state.chat_history.append(AIMessage(content=ai_response))

        response = f"Genie: {ai_response}"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.previous_messages.append(
            {"role": "assistant", "content": response}
        )


if __name__ == "__main__":
    main()
