# AskPhilosopher
AskPhilosopher is a browser-based chat application for philosophy, incorporating a fine-tuned TinyLlama model enhanced with Retrieval-Augmented Generation (RAG).


<img width="1147" height="722" alt="Screenshot 2025-07-10 at 11 40 41 PM" src="https://github.com/user-attachments/assets/e5fd9752-3c93-42c3-aafc-866bb40c7a50" />

## Features
-   **Fine-Tuned LLM**: Utilizes a version of TinyLlama fine-tuned on synthetic philosophy conversational data.
-   **Retrieval-Augmented Generation (RAG)**: Enhances model responses by retrieving relevant information from a vector database of philosophy books and providing it as context to the model.
-   **Flask API**: A simple and robust backend built with Flask to serve the chatbot.
-   **Web application**: A lightweight user interface enabling general access, testing, and experimentation with the philosophy chatbot

## Technology Stack
-   **Frontend**: React, JavaScript, CSS
-   **Backend**: Python, Flask
-   **ML/DL**: PyTorch, Hugging Face `transformers`, `peft`
-   **RAG**: A vector store (e.g. langchain, FAISS) is used for similarity search. The `rag_db_creation.py` script handles the creation of this database.

## Project Structure
```
├── backend
│   ├── app.py                                                # Main Flask application and API endpoint
│   └── rag_db_creation.py                                    # Script to create the vector store for RAG
├── AskPhilosopher/                                           # React application
│   └── ...
├── fine-tune-custom-philosophy-chatbot-llama-phi-2.ipynb     # Training notebook
└── README.md
```
