from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def ask_ai(messages, document_text=""):

    final_messages = []

    if document_text:

        final_messages.append({
            "role": "system",
            "content": f"""
The user uploaded the following document.

Use it to answer questions.

Document:

{document_text}
"""
        })

    final_messages.extend(messages)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=final_messages
    )

    return response.choices[0].message.content