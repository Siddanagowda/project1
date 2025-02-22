import streamlit as st
from rag_pipeline import RAGPipeline
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if 'rag' not in st.session_state:
    st.session_state.rag = RAGPipeline()
    # Try to load existing state
    if os.path.exists("saved_state"):
        st.session_state.rag.load_state()

def main():
    st.title("News Article RAG System")
    st.write("A smart news assistant powered by Google's Gemini")

    # Sidebar
    with st.sidebar:
        st.header("Controls")
        
        # Scraping section
        st.subheader("Scrape Articles")
        num_articles = st.slider("Number of articles to scrape", 1, 10, 3)
        if st.button("Scrape Articles"):
            with st.spinner("Scraping articles..."):
                try:
                    # Scrape articles
                    articles = st.session_state.rag.scraper.scrape_articles(limit=num_articles)
                    
                    # Display scraped articles
                    st.write(f"Found {len(articles)} articles:")
                    for article in articles:
                        with st.expander(article['title']):
                            st.write(f"Source: {article['url']}")
                            st.write(f"Length: {len(article['content'])} characters")
                            st.write("Preview:")
                            st.write(article['content'][:200] + "...")
                    
                    # Index the articles
                    with st.spinner("Indexing articles..."):
                        documents = st.session_state.rag.vector_store.create_documents(articles)
                        st.session_state.rag.vector_store.index_documents(documents)
                        
                    # Save state
                    st.session_state.rag.save_state()
                    st.success("Articles scraped and indexed successfully!")
                    
                except Exception as e:
                    st.error(f"Error during scraping: {str(e)}")
        
        # Save/Load section
        st.subheader("Save/Load")
        if st.button("Save State"):
            with st.spinner("Saving state..."):
                st.session_state.rag.save_state()
                st.success("State saved successfully!")
        
        if st.button("Load State"):
            with st.spinner("Loading state..."):
                st.session_state.rag.load_state()
                st.success("State loaded successfully!")

    # Main chat interface
    st.header("Chat with Your News Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("sources"):
                st.write("\nSources:")
                for source in message["sources"]:
                    st.write(f"- [{source['title']}]({source['url']})")

    # Chat input
    if prompt := st.chat_input("Ask about the news"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.rag.generate_response(prompt)
                    st.write(response["answer"])
                    
                    if response["sources"]:
                        st.write("\nSources:")
                        for source in response["sources"]:
                            st.write(f"- [{source['title']}]({source['url']})")
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response["sources"]
                    })
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()
