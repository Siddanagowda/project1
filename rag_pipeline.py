from typing import Dict, List
from scraper import NewsArticleScraper
from vectorstore import VectorStore
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGPipeline:
    def __init__(self):
        """Initialize the RAG pipeline components."""
        self.scraper = NewsArticleScraper()
        self.vector_store = VectorStore()
        
        # Initialize Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config={
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
        )
        
        # Initialize chat history
        self.chat_history = []
    
    def scrape_and_index(self, limit: int = 5):
        """Scrape articles and index them in the vector store."""
        articles = self.scraper.scrape_articles(limit=limit)
        if articles:
            documents = self.vector_store.create_documents(articles)
            self.vector_store.index_documents(documents)
        return len(articles)

    def generate_response(self, query: str, k: int = 3) -> Dict:
        """Generate a response using RAG."""
        try:
            # Get relevant documents
            relevant_docs = self.vector_store.similarity_search(query, k=k)
            
            if not relevant_docs:
                return {
                    "answer": "I don't have any relevant articles to answer your question. Try scraping some articles first.",
                    "sources": []
                }
            
            # Format context from relevant documents
            context = "\n\n".join([
                f"Article: {doc['title']}\n{doc['content'][:500]}..."
                for doc in relevant_docs
            ])
            
            # Create prompt with chat history context
            chat_context = "\n".join([
                f"User: {exchange['user']}\nAssistant: {exchange['assistant']}"
                for exchange in self.chat_history[-3:]  # Include last 3 exchanges
            ])
            
            prompt = f"""You are a helpful AI assistant that answers questions based on the provided news articles.
            Your responses should be informative and well-structured, based solely on the context provided.
            If the context doesn't contain enough information to answer the question, say so.

            Previous conversation:
            {chat_context}

            Relevant articles:
            {context}

            User question: {query}

            Please provide a comprehensive answer based on the articles above."""

            # Generate response
            response = self.model.generate_content(prompt)
            
            # Update chat history
            self.chat_history.append({
                "user": query,
                "assistant": response.text
            })
            
            return {
                "answer": response.text,
                "sources": [
                    {
                        "title": doc["title"],
                        "url": doc["url"],
                        "timestamp": doc["timestamp"]
                    }
                    for doc in relevant_docs
                ]
            }
            
        except Exception:
            return {
                "answer": "I encountered an error while generating the response. Please try again.",
                "sources": []
            }
    
    def save_state(self, directory: str = "saved_state"):
        """Save the current state of the RAG pipeline."""
        os.makedirs(directory, exist_ok=True)
        self.vector_store.save_vector_store(f"{directory}/vector_store")
    
    def load_state(self, directory: str = "saved_state"):
        """Load a previously saved state of the RAG pipeline."""
        self.vector_store.load_vector_store(f"{directory}/vector_store")
