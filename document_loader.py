import fitz
from docx import Document


def extract_text(uploaded_file):
    """
    Extract text from PDF, DOCX, or TXT files.
    """

    text = ""

    if uploaded_file is None:
        return text

    if uploaded_file.type == "application/pdf":

        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        for page in pdf:
            text += page.get_text()

    elif uploaded_file.type == "text/plain":

        text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

        doc = Document(uploaded_file)

        for para in doc.paragraphs:
            text += para.text + "\n"

    return text