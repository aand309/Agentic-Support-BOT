
# Agentic Customer Support Bot



##  Objective

[cite_start]This project is an implementation of an agentic workflow in Python for a customer support bot[cite: 3]. [cite_start]The bot is designed to train on a provided document (like a company FAQ), answer customer queries based on that document's content, and iteratively refine its responses using simulated feedback[cite: 3]. [cite_start]The core logic is built using the LangChain framework to manage document processing and interactions with NLP models[cite: 20].

## ✨ Features

* [cite_start]**Document Training**: Ingests and processes text from a source document like an FAQ or manual[cite: 7].
* [cite_start]**Semantic Search**: Uses `sentence-transformers` embeddings and a FAISS vector store to find the most relevant document sections for a given query[cite: 18].
* [cite_start]**Question Answering**: Leverages a pre-trained Hugging Face model (`distilbert-base-uncased-distilled-squad`) to extract answers from the retrieved context[cite: 8, 17].
* [cite_start]**Adaptive Feedback Loop**: Simulates user feedback (e.g., "good," "too vague," "not helpful") and adjusts its response strategy accordingly[cite: 9, 10, 41, 42].
* [cite_start]**Transparent Logging**: Logs all major actions, decisions, and feedback to `support_bot_log.txt` for traceability and debugging[cite: 11, 21].
* [cite_start]**Robust Query Handling**: Provides a graceful fallback response for queries that are not covered in the source document[cite: 12].

##  Project Structure

```

.
├── .gitignore
├── README.md
├── data
│   └── faq.txt
├── main.py
├── requirements.txt
├── src
│   └── bot.py
└── support\_bot\_log.txt

````

##  Technologies Used

* **Language**: Python
* **Core Framework**: LangChain
* **NLP Models**: Hugging Face Transformers (`pipeline`)
* **Text Embeddings**: Sentence-Transformers
* **Vector Store**: FAISS (Facebook AI Similarity Search)

##  Setup and Installation

Follow these steps to set up and run the project locally.

#### Prerequisites

* Python 3.10+
* Git

#### 1. Clone the repository

```bash
git clone [https://github.com/aand309/Agentic-Support-BOT.git](https://github.com/aand309/Agentic-Support-BOT.git)
cd Agentic-Support-BOT
````

#### 2\. Create a virtual environment

It's highly recommended to use a virtual environment to manage project dependencies.

  * On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
  * On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

#### 3\. Install dependencies

Install all the necessary libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

##  How to Run

To start the bot, simply run the `main.py` script from the root directory of the project:

```bash
python main.py
```

The bot will process the sample queries defined in `main.py`, print its initial and updated responses to the console, and generate a clean `support_bot_log.txt` file with the details of the run.

##  How It Works

The bot uses a **Retrieval-Augmented Generation (RAG)** approach:

1.  [cite\_start]**Loading**: The `faq.txt` document is loaded and split into logical chunks based on its structure[cite: 30, 34].
2.  [cite\_start]**Embedding & Storage**: Each chunk is converted into a numerical vector (embedding) and stored in a FAISS vector store for efficient similarity searching[cite: 35].
3.  **Retrieval**: When you ask a query, the bot converts the query into an embedding and uses FAISS to find the most semantically similar text chunk from the document. It also checks a similarity score to ensure the chunk is relevant enough to answer the question.
4.  [cite\_start]**Generation**: The original query and the retrieved text chunk are passed to a pre-trained Question-Answering model from Hugging Face, which then extracts the final answer[cite: 38].
5.  [cite\_start]**Feedback Loop**: The bot simulates feedback on its answer and can re-attempt the query with a modified strategy if the feedback is negative[cite: 41, 42].

##  Future Improvements

  * **Conversational Memory**: Integrate a memory component to allow the bot to handle follow-up questions and maintain context across a conversation.
  * **Advanced Feedback Handling**: Use another LLM call to interpret the feedback more intelligently and generate a more nuanced, revised response.
  * **UI Integration**: Build a simple web interface (e.g., using Flask or Streamlit) to interact with the bot in a more user-friendly way.

<!-- end list -->

```
```
