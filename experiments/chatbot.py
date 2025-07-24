import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama(question):
    payload = {
        "model": "llama3",
        "prompt": question,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response received.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

def main():
    st.title("AP Physics C Chatbot")
    st.write("Ask your AP Physics C questions and get answers!")

    question = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a question first!")
        else:
            with st.spinner("Thinking..."):
                answer = query_ollama(question)
            st.markdown("**Answer:**")
            st.write(answer)

if __name__ == "__main__":
    main()
