# Finay: Professional News Research Tool

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

For issues or questions, please open an issue on GitHub.