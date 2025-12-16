"""''''''''''''''''''''''''''''''''

@st.cache_resource
def setup():
    raw = load_doctors()
    texts = prepare_documents(raw)
    print("------------------Texts-----------------------------------------")
    print(texts[0])
    print("-----------------------------------------------------------")
    chunks = chunk_documents(texts)
    print("=============================Chunks================================")
    print(chunks[0])
    print("=============================================================")
    embeddings = embed_texts([c["text"] for c in chunks])
    print(len(embeddings[0]))
    client = get_client()
    create_collection(client, len(embeddings[0]))
    store_chunks(client, chunks, embeddings)

    return client

client = setup()

st.title("پیشنهاد دکتر متخصص براساس نیازمندی شما:", text_alignment="right")

query = st.text_input("سوال خود را مطرح نمایید :")

if query:
    answer, context = answer_query(client, query)

    st.subheader("پاسخ",text_alignment="right")
    st.write(answer)

    with st.expander("Retrieved Context"):
        for c in context:
            st.write(c)

'''''''''''''''''''''''''''''''"""
import streamlit as st
from Src.load_data import load_doctors, prepare_documents
from Src.Embedding_And_vector_store import chunk_documents,embed_texts
from Src.Embedding_And_vector_store import get_client, create_collection, store_chunks
from Src.RAG_Pipeline import answer_query

# Make Css for Right to left writing
st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
        font-family: BZar, Tahoma, Geneva, sans-serif;
    }

    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {
        direction: rtl;
        text-align: right;
    }

    /* Chat messages */
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }

    /* Input box */
    textarea {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title="سامانه پیشنهاد دهنده متخصص")

@st.cache_resource
def setup():
    raw = load_doctors()
    texts = prepare_documents(raw)
    chunks = chunk_documents(texts)
    embeddings = embed_texts([c["text"] for c in chunks])
    client = get_client()
    create_collection(client, len(embeddings[0]))
    store_chunks(client, chunks, embeddings)
    return client

client = setup()

st.title("پیشنهاد دکتر متخصص براساس نیازمندی شما:")

# chat memory 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام. مشکل یا نیازتان را توضیح دهید تا متخصص مناسب را پیشنهاد کنم."}
    ]

# render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_text = st.chat_input("سوال خود را مطرح نمایید...")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    answer, context = answer_query(client, user_text, chat_history=st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)
        with st.expander("Retrieved Context"):
            for c in context:
                st.write(c)

with st.sidebar:
    if st.button("پاک کردن گفتگو"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()
