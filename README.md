# 🌐 News Article RAG Application

This application implements a Retrieval-Augmented Generation (RAG) pipeline that scrapes news articles from various sources, indexes them in a FAISS vector database, and allows users to query the articles using natural language. It generates contextual responses using Google's Gemini model.

## 📚 Table of Contents
- [✨ Features](#features)
- [🔧 Setup](#setup)
- [🚀 Usage](#usage)
- [🛠 Components](#components)
- [💻 Example Run](#example-run)
- [🤝 Contributing](#contributing)
- [📄 License](#license)

## ✨ Features
- 📰 Scrapes news articles from multiple sources
- 📚 Indexes articles for efficient retrieval
- 🤖 Generates responses to user queries using advanced AI
- 🌟 User-friendly web interface built with Streamlit

## 🔧 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Siddanagowda/project1.git
   cd project1
   ```

2. Create a `.env` file in the root directory with your Google API key:
   ```plaintext
   GOOGLE_API_KEY=your_api_key_here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Use the sidebar to scrape articles and ask questions about the news.

## 🛠 Components

- **scraper.py**: Contains the web scraping logic for fetching news articles.
- **vectorstore.py**: Handles document indexing and vector storage using FAISS.
- **rag_pipeline.py**: Implements the RAG pipeline using LangChain and Gemini.
- **streamlit_app.py**: Provides a modern web interface for user interaction.

## 💻 Example Run

1. **Scrape Articles**:
   - Use the slider in the sidebar to select the number of articles to scrape (1-10).
   - Click the "Scrape Articles" button to fetch articles from the configured sources.

2. **Ask Questions**:
   - In the chat interface, enter a question about the news.
   - Click "Send" to receive a response generated based on the scraped articles.

### Example Questions:
- "What are the latest headlines in technology? 📰"
- "Can you summarize the latest news about AI? 🤖"

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
