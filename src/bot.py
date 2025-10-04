# src/bot.py

import logging
import random
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from transformers import pipeline

# --- CHANGE IS HERE: Added mode='w' to create a fresh log file on each run ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("support_bot_log.txt", mode='w'),
        logging.StreamHandler()
    ]
)

class SupportBotAgent:
    def __init__(self, document_path: str):
        logging.info(f"Initializing SupportBotAgent with document: {document_path}")
        self.document_path = document_path
        self._setup_pipeline()

    def _setup_pipeline(self):
        loader = TextLoader(self.document_path)
        documents = loader.load()
        logging.info(f"Successfully loaded document: {self.document_path}")

        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=200,
            chunk_overlap=0,
            length_function=len,
        )
        docs = text_splitter.split_documents(documents)

        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        
        self.vector_store = FAISS.from_documents(docs, embeddings)

        self.qa_pipeline = pipeline(
            "question-answering",
            model="distilbert-base-uncased-distilled-squad",
            tokenizer="distilbert-base-uncased-distilled-squad"
        )
        logging.info("Pipeline setup complete.")

    def answer_query(self, query: str) -> str:
        logging.info(f"Received query: '{query}'")
        docs_with_scores = self.vector_store.similarity_search_with_score(query, k=1)

        if not docs_with_scores or docs_with_scores[0][1] > 1.0:
            logging.warning(f"No relevant context found for query: '{query}'. Best match score was too high.")
            return "I don't have enough information to answer that."

        relevant_docs = [docs_with_scores[0][0]]
        context = " ".join([doc.page_content for doc in relevant_docs])
        
        result_dict = self.qa_pipeline(question=query, context=context)
        answer = result_dict.get("answer", "")

        if not answer.strip():
            logging.warning(f"QA model could not find an answer for query: '{query}'")
            return "I don't have enough information to answer that."

        logging.info(f"Generated answer: '{answer}'")
        return answer

    def simulate_feedback(self) -> str:
        feedback = random.choice(["good", "not helpful", "too vague"])
        logging.info(f"Simulated feedback received: '{feedback}'")
        return feedback

    def adjust_response(self, query: str, response: str, feedback: str) -> str:
        logging.info(f"Adjusting response based on feedback: '{feedback}'")
        if feedback == "too vague":
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=1)
            if docs_with_scores and docs_with_scores[0][1] <= 1.0:
                context = docs_with_scores[0][0].page_content
                return f"{response}\n\nHere is some more context: {context}"
            return f"{response} (Could not retrieve additional context.)"
        elif feedback == "not helpful":
            rephrased_query = f"Can you give me more details about: {query}"
            logging.info(f"Rephrasing query to: '{rephrased_query}'")
            return self.answer_query(rephrased_query)
        
        return response

    def run(self, queries: list[str]):
        for query in queries:
            print(f"\n--- Processing Query: '{query}' ---")
            logging.info(f"--- New Query Processing Started: '{query}' ---")
            
            initial_response = self.answer_query(query)
            print(f"🤖 Initial Response: {initial_response}")

            response = initial_response
            for i in range(2):
                feedback = self.simulate_feedback()
                if feedback == "good":
                    logging.info("Feedback was 'good'. Ending feedback loop.")
                    print("👍 Feedback: Good!")
                    break
                
                print(f"🤔 Feedback: {feedback}. Refining answer...")
                response = self.adjust_response(query, response, feedback)
                print(f"🤖 Updated Response ({i+1}): {response}")
            
            logging.info(f"--- Query Processing Finished for: '{query}' ---")