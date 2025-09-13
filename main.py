import os
import streamlit as st
import pickle
import time

# Try to import required libraries
try:
    from langchain.llms import OpenAI
    from langchain.chains import RetrievalQAWithSourcesChain
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.document_loaders import UnstructuredURLLoader
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
except ImportError as e:
    st.error(f"Missing required library: {e}")
    st.info("Please install required libraries using: pip install langchain openai faiss-cpu streamlit python-dotenv unstructured")
    st.stop()

from dotenv import load_dotenv
load_dotenv()

# Check for API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OpenAI API Key not found!")
    st.info("Please create a .env file with: OPENAI_API_KEY=your-key-here")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Finay - News Research Tool",
    page_icon="📊",
    layout="wide"
)

# Simple styling
st.markdown("""
<style>
    .main { padding: 2rem; }
    h1 { color: #37352F; font-size: 2.5rem; }
    .subtitle { color: #787774; font-size: 1.1rem; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Finay")
st.markdown("Professional News Research & Analysis Tool")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Article Sources")
    st.caption("Enter up to 3 article URLs for analysis")
    
    urls = []
    for i in range(3):
        url = st.text_input(f"URL {i+1}", placeholder="https://example.com/article")
        if url:
            urls.append(url)
    
    process_button = st.button("Process Articles", type="primary", use_container_width=True)

# Initialize LLM
llm = OpenAI(temperature=0.9, max_tokens=500)
file_path = "faiss_store.pkl"

# Process URLs
if process_button and urls:
    with st.spinner("Processing articles..."):
        try:
            # Load data
            loader = UnstructuredURLLoader(urls=urls)
            data = loader.load()
            
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '.', ','],
                chunk_size=1000
            )
            docs = text_splitter.split_documents(data)
            
            # Create embeddings
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(docs, embeddings)
            
            # Save index
            with open(file_path, "wb") as f:
                pickle.dump(vectorstore, f)
            
            st.success("✅ Articles processed successfully!")
        except Exception as e:
            st.error(f"Error processing articles: {e}")

# Query section
st.header("Ask a Question")
query = st.text_input("Enter your question about the articles:", placeholder="What are the main topics discussed?")

if query:
    if os.path.exists(file_path):
        with st.spinner("Finding answer..."):
            try:
                # Load vectorstore
                with open(file_path, "rb") as f:
                    vectorstore = pickle.load(f)
                
                # Create chain and get answer
                chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
                result = chain({"question": query}, return_only_outputs=True)
                
                # Display results
                st.header("Answer")
                st.write(result['answer'])
                
                if result.get('sources'):
                    st.header("Sources")
                    for source in result['sources'].split('\n'):
                        if source:
                            st.caption(source)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please process some articles first!")