import streamlit as st
from openai import OpenAI
import fitz
from docx import Document
import time

# =========================================================
# NVIDIA API CONFIGURATION
# =========================================================

NVIDIA_API_KEY = "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"

client = OpenAI(
    api_key=NVIDIA_API_KEY,
    base_url="https://integrate.api.nvidia.com/v1"
)

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SONIS AI",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

h1 {
    text-align: center;
}

.stChatMessage {
    border-radius: 18px;
    padding: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 SONIS AI")

    st.markdown("---")

    st.write("### 🚀 AI Assistant")

    st.write("""
Powered by:

- ⚡ NVIDIA NIM
- 🧠 Nemotron 3 Super 120B
- 🎈 Streamlit
""")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 📎 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX or TXT file",
        type=["pdf", "docx", "txt"]
    )

# =========================================================
# DOCUMENT EXTRACTION
# =========================================================

document_text = ""

if uploaded_file is not None:

    if uploaded_file.type == "application/pdf":

        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        for page in pdf:
            document_text += page.get_text()

        pdf.close()

    elif uploaded_file.type == "text/plain":

        document_text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

        doc = Document(uploaded_file)

        for para in doc.paragraphs:
            document_text += para.text + "\n"

    st.success("✅ Document uploaded successfully!")

    with st.expander("📄 Preview"):
        st.text(document_text[:5000])

# =========================================================
# MAIN TITLE
# =========================================================

st.title("🤖 SONIS AI")
st.caption("Your Personal AI Assistant")

# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.info("👋 Welcome! Ask me anything.")

    c1, c2 = st.columns(2)

    with c1:

        if st.button("🐍 Explain Python"):
            st.session_state.example = "Explain Python"

    with c2:

        if st.button("😂 Tell me a joke"):
            st.session_state.example = "Tell me a joke"

# =========================================================
# SHOW CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    avatar = "👨🏻‍💻" if message["role"] == "user" else "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])

# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input("Message SONIS AI...")

if "example" in st.session_state:

    prompt = st.session_state.example

    del st.session_state.example

# =========================================================
# GENERATE RESPONSE
# =========================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user", avatar="👨🏻‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        thinking = st.empty()
        thinking.info("🧠 Thinking...")

        start = time.time()

        messages = []

        if document_text:

            messages.append(
                {
                    "role": "system",
                    "content": f"""
You are SONIS AI.

The user has uploaded a document.

When the user asks something related to the uploaded
document, use the document as your primary source.

If the answer cannot be found in the document, clearly
say that the information is not present in the document.

Uploaded document:

{document_text}
"""
                }
            )

        messages.extend(st.session_state.messages)

        try:

            response = client.chat.completions.create(
                model="nvidia/nemotron-3-super-120b-a12b",
                messages=messages,
                temperature=0.5,
                top_p=1,
                max_tokens=1024,
                stream=True
            )

            reply = ""

            placeholder = st.empty()

            first_chunk = True

            for chunk in response:

                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0].delta.content
                ):

                    if first_chunk:
                        thinking.empty()
                        first_chunk = False

                    content = chunk.choices[0].delta.content

                    reply += content

                    placeholder.markdown(
                        reply + " ▌"
                    )

            placeholder.markdown(reply)

            end = time.time()

            st.caption(
                f"⚡ Generated in {end - start:.2f} seconds"
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

        except Exception as e:

            thinking.empty()

            st.error(
                f"❌ NVIDIA API Error: {str(e)}"
            )