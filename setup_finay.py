#!/usr/bin/env python3
"""
Finay - Professional News Research Tool
Automated Setup Script
"""

import os
import sys
import subprocess

def create_file(path, content):
    """Create a file with the given content"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {path}")

def create_directory(path):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✓ Created directory: {path}")

# Main application code
MAIN_PY = '''import os
import streamlit as st
import pickle
import time
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Finay - News Research Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Notion-like styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Title styling */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: #37352F;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        border-bottom: none;
        padding-bottom: 0;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #787774;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #FBFBFA;
        padding: 2rem 1rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        border: 1px solid #E1E1DB;
        border-radius: 3px;
        padding: 8px 12px;
        font-size: 14px;
        color: #37352F;
        transition: border-color 0.2s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E81F4;
        box-shadow: 0 0 0 1px #2E81F4;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2E81F4;
        color: white;
        border: none;
        border-radius: 3px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 500;
        transition: background-color 0.2s;
        width: 100%;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: #0F7BFF;
    }
    
    /* Processing status */
    .status-box {
        background-color: #F7F6F3;
        border-left: 3px solid #2E81F4;
        padding: 12px 16px;
        margin: 1rem 0;
        border-radius: 3px;
        font-size: 14px;
        color: #37352F;
    }
    
    /* Answer section */
    .answer-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #37352F;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    .answer-content {
        background-color: #FFFFFF;
        border: 1px solid #E1E1DB;
        border-radius: 3px;
        padding: 1.5rem;
        line-height: 1.6;
        color: #37352F;
    }
    
    /* Source section */
    .source-item {
        background-color: #F7F6F3;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 3px;
        font-size: 13px;
        color: #787774;
        word-break: break-all;
    }
    
    /* Sidebar header */
    .sidebar-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #37352F;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E1E1DB;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        .subtitle {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main title and subtitle
st.markdown("<h1>Finay</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Professional News Research & Analysis Tool</p>", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("<div class='sidebar-header'>Article Sources</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #787774; font-size: 13px; margin-bottom: 1rem;'>Enter up to 3 article URLs for analysis</p>", unsafe_allow_html=True)
    
    urls = []
    for i in range(3):
        url = st.text_input(
            f"URL {i+1}",
            placeholder="https://example.com/article",
            key=f"url_{i}",
            label_visibility="collapsed"
        )
        if url:
            urls.append(url)
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    process_url_clicked = st.button("Process Articles", use_container_width=True)
    
    # Additional information
    st.markdown("<div style='margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #E1E1DB;'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #787774; font-size: 12px;'><strong>About Finay</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #787774; font-size: 12px; line-height: 1.5;'>Finay uses advanced NLP to analyze news articles and provide intelligent responses to your queries with source citations.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# File path for vector store
file_path = "faiss_store_openai.pkl"

# Main content area
main_placeholder = st.empty()

# Initialize LLM
llm = OpenAI(temperature=0.9, max_tokens=500)

# Process URLs
if process_url_clicked:
    if not any(urls):
        st.error("Please enter at least one URL to process.")
    else:
        # Filter out empty URLs
        valid_urls = [url for url in urls if url.strip()]
        
        with st.spinner(""):
            # Load data
            loader = UnstructuredURLLoader(urls=valid_urls)
            main_placeholder.markdown("<div class='status-box'>Loading article content...</div>", unsafe_allow_html=True)
            data = loader.load()
            time.sleep(1)
            
            # Split data
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\\n\\n', '\\n', '.', ','],
                chunk_size=1000
            )
            main_placeholder.markdown("<div class='status-box'>Processing text segments...</div>", unsafe_allow_html=True)
            docs = text_splitter.split_documents(data)
            time.sleep(1)
            
            # Create embeddings
            embeddings = OpenAIEmbeddings()
            vectorstore_openai = FAISS.from_documents(docs, embeddings)
            main_placeholder.markdown("<div class='status-box'>Building knowledge index...</div>", unsafe_allow_html=True)
            time.sleep(2)
            
            # Save FAISS index
            with open(file_path, "wb") as f:
                pickle.dump(vectorstore_openai, f)
            
            main_placeholder.markdown("<div class='status-box' style='border-left-color: #22C55E;'>Processing complete. Ready for queries.</div>", unsafe_allow_html=True)

# Query interface
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Ask a question about the articles",
        placeholder="What are the key points discussed in the articles?",
        label_visibility="collapsed"
    )

# Process query
if query:
    if os.path.exists(file_path):
        with st.spinner("Analyzing..."):
            with open(file_path, "rb") as f:
                vectorstore = pickle.load(f)
                chain = RetrievalQAWithSourcesChain.from_llm(
                    llm=llm, 
                    retriever=vectorstore.as_retriever()
                )
                result = chain({"question": query}, return_only_outputs=True)
                
                # Display answer
                st.markdown("<div class='answer-header'>Response</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='answer-content'>{result['answer']}</div>", unsafe_allow_html=True)
                
                # Display sources if available
                sources = result.get("sources", "")
                if sources:
                    st.markdown("<div class='answer-header'>Sources</div>", unsafe_allow_html=True)
                    sources_list = sources.split("\\n")
                    for source in sources_list:
                        if source.strip():
                            st.markdown(f"<div class='source-item'>{source}</div>", unsafe_allow_html=True)
    else:
        st.info("Please process articles first by entering URLs in the sidebar and clicking 'Process Articles'.")

# Footer information
st.markdown("<div style='margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #E1E1DB;'>", unsafe_allow_html=True)
st.markdown("<p style='color: #787774; font-size: 12px; text-align: center;'>Finay - Professional News Research Tool</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)'''

# Requirements file
REQUIREMENTS_TXT = '''langchain==0.0.284
python-dotenv==1.0.0
streamlit==1.22.0
unstructured==0.9.2
tiktoken==0.4.0
faiss-cpu==1.7.4
libmagic==1.0
python-magic==0.4.27
python-magic-bin==0.4.14
OpenAI==0.28.0'''

# README file
README_MD = '''# Finay: Professional News Research Tool

Finay is a sophisticated news research tool designed for seamless information retrieval and analysis. Users can input article URLs and ask questions to receive intelligent insights from financial and business news domains.

## Overview

Finay leverages advanced natural language processing to analyze news articles and provide accurate, source-cited responses to user queries. The interface features a clean, Notion-inspired design that prioritizes functionality and professional aesthetics.

## Features

- **Multi-URL Processing**: Load up to 3 article URLs simultaneously for comprehensive analysis
- **Advanced Text Processing**: Utilizes LangChain's UnstructuredURL Loader for robust content extraction
- **Intelligent Embeddings**: Constructs embedding vectors using OpenAI's embeddings combined with FAISS for efficient similarity search
- **Source Attribution**: Provides transparent source citations for all generated responses
- **Professional Interface**: Clean, minimalist design inspired by Notion's aesthetic principles
- **Persistent Storage**: Saves processed embeddings locally for quick retrieval

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/finay.git
```

2. Navigate to the project directory:

```bash
cd finay
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key by creating a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the Streamlit application:

```bash
streamlit run main.py
```

2. The application will open in your default web browser

3. Using Finay:
   - Enter up to 3 article URLs in the sidebar
   - Click "Process Articles" to analyze the content
   - Wait for the processing to complete
   - Enter your question in the main input field
   - Receive comprehensive answers with source citations

## Project Structure

```
finay/
│
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── faiss_store_openai.pkl # Saved FAISS index (generated)
└── README.md              # Documentation
```

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please open an issue on GitHub.'''

# .gitignore file
GITIGNORE = '''# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Pickle files (vector stores)
*.pkl
faiss_store_openai.pkl
vector_index.pkl

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/'''

# .env template
ENV_TEMPLATE = '''# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Add your actual OpenAI API key above'''

def main():
    print("\n" + "="*60)
    print("FINAY - Professional News Research Tool")
    print("Automated Setup Script")
    print("="*60 + "\n")
    
    # Get the directory where the script is run
    base_dir = os.getcwd()
    finay_dir = os.path.join(base_dir, 'finay')
    
    # Ask user if they want to create in current directory or new directory
    choice = input("Create Finay in:\n1. Current directory\n2. New 'finay' directory\nChoice (1 or 2): ").strip()
    
    if choice == '2':
        create_directory(finay_dir)
        os.chdir(finay_dir)
        print(f"\n✓ Working directory: {finay_dir}")
    else:
        print(f"\n✓ Working directory: {base_dir}")
    
    # Create notebooks directory
    create_directory("notebooks")
    
    # Create all necessary files
    print("\nCreating project files...")
    create_file("main.py", MAIN_PY)
    create_file("requirements.txt", REQUIREMENTS_TXT)
    create_file("README.md", README_MD)
    create_file(".gitignore", GITIGNORE)
    create_file(".env", ENV_TEMPLATE)
    
    # Create placeholder for vector_index.pkl
    create_file("notebooks/.gitkeep", "# This file ensures the notebooks directory is tracked by git")
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. If you have a vector_index.pkl file, copy it to the notebooks/ folder")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run the application: streamlit run main.py")
    
    print("\n💡 QUICK COMMANDS:")
    print("-"*40)
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("# Create virtual environment (recommended):")
        if os.name == 'nt':  # Windows
            print("python -m venv venv")
            print("venv\\Scripts\\activate")
        else:  # Mac/Linux
            print("python3 -m venv venv")
            print("source venv/bin/activate")
        print()
    
    print("# Install dependencies:")
    print("pip install -r requirements.txt")
    print()
    print("# Run Finay:")
    print("streamlit run main.py")
    
    print("\n" + "="*60)
    
    # Ask if user wants to install dependencies now
    install_now = input("\n🚀 Install dependencies now? (y/n): ").strip().lower()
    if install_now == 'y':
        print("\nInstalling dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("\n✅ Dependencies installed successfully!")
            
            # Ask if user wants to run the app
            run_now = input("\n🎯 Run Finay now? (y/n): ").strip().lower()
            if run_now == 'y':
                print("\n⚠️  IMPORTANT: Make sure to add your OpenAI API key to the .env file first!")
                input("Press Enter when you've added your API key...")
                print("\nStarting Finay...")
                subprocess.run(["streamlit", "run", "main.py"])
        except subprocess.CalledProcessError:
            print("\n⚠️  Error installing dependencies. Please install manually:")
            print("pip install -r requirements.txt")
    
    print("\n✨ Setup script completed!")

if __name__ == "__main__":
    main()