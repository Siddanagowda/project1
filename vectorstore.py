from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle
from datetime import datetime

class VectorStore:
    def __init__(self):
        """Initialize the vector store with TF-IDF vectorizer."""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        self.documents = []
        self.document_embeddings = None

    def create_documents(self, articles: List[Dict]) -> List[Dict]:
        """Convert articles to documents."""
        documents = []
        for article in articles:
            doc = {
                "content": f"{article['title']}\n\n{article['content']}",
                "metadata": {
                    "title": article["title"],
                    "url": article["url"],
                    "timestamp": article["timestamp"],
                    "source": article.get("source", "unknown")
                }
            }
            documents.append(doc)
        return documents

    def index_documents(self, documents: List[Dict]) -> None:
        """Index documents using TF-IDF vectorization."""
        if not documents:
            return

        self.documents = documents
        texts = [doc["content"] for doc in documents]
        
        # Generate document embeddings
        self.document_embeddings = self.vectorizer.fit_transform(texts)

    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar documents using cosine similarity."""
        if not self.documents or self.document_embeddings is None:
            return []

        try:
            # Generate query embedding
            query_embedding = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(
                query_embedding, 
                self.document_embeddings
            ).flatten()
            
            # Get top k most similar documents
            most_similar_indices = similarities.argsort()[-k:][::-1]
            
            # Convert to the expected format
            results = []
            for idx in most_similar_indices:
                doc = self.documents[idx]
                results.append({
                    "title": doc["metadata"]["title"],
                    "url": doc["metadata"]["url"],
                    "timestamp": doc["metadata"]["timestamp"],
                    "content": doc["content"],
                    "similarity": float(similarities[idx])
                })
            
            return results
            
        except Exception as e:
            return []

    def save_vector_store(self, path: str = "vector_store") -> None:
        """Save the vector store to disk."""
        os.makedirs(path, exist_ok=True)
        
        # Save components
        with open(f"{path}/vectorizer.pkl", "wb") as f:
            pickle.dump(self.vectorizer, f)
        
        with open(f"{path}/documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)
        
        if self.document_embeddings is not None:
            with open(f"{path}/embeddings.pkl", "wb") as f:
                pickle.dump(self.document_embeddings, f)

    def load_vector_store(self, path: str = "vector_store") -> None:
        """Load the vector store from disk."""
        try:
            if not os.path.exists(path):
                return
            
            # Load components
            with open(f"{path}/vectorizer.pkl", "rb") as f:
                self.vectorizer = pickle.load(f)
            
            with open(f"{path}/documents.pkl", "rb") as f:
                self.documents = pickle.load(f)
            
            if os.path.exists(f"{path}/embeddings.pkl"):
                with open(f"{path}/embeddings.pkl", "rb") as f:
                    self.document_embeddings = pickle.load(f)
            
        except Exception:
            # Reset state on error
            self.__init__()
