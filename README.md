# Document Genie - A Generative AI PDF Chatbot

Welcome to **Product Builders** where we dive into the world of generative AI. Today, we are unveiling something truly exciting: a step-by-step tutorial on building your own Chat PDF, which we have lovingly named **Document Genie**.

## Introduction
Document Genie is a chatbot built using the RAG (Retrieval-Augmented Generation) framework leveraging the generative AI model Gemini Pro. It processes your PDF documents by breaking them into manageable chunks, creating a searchable vector store, and generating accurate answers to your queries.

## Features
- **Enter your Google API Key**: Securely input your API key.
- **Upload Document**: Upload your PDF on the sidebar.
- **Ask Questions**: Inquire about any content within your document.

## Getting Started

### Step 1: Obtain Google API Key
2. Create your API key and save it securely.
3. Enter your API key in the app.

### Step 2: Upload a PDF
1. Use the file uploader to upload any PDF document.
2. Click on "Submit and Process".

### Step 3: Ask Questions
1. Once processed, ask questions related to your document.
2. Example: "How to use Canva AI?"

## How It Works
### RAG Framework
- **Retrieval**: Searches external databases for related information.
- **Augmentation**: Enriches the prompt with factual context.
- **Generation**: Produces accurate, context-aware responses.

### Embeddings
- Converts text into mathematical representations.
- Uses vector databases to find similar texts.
- Ensures relevant context alignment with user queries.

## Code Walkthrough
### Libraries
- **PyPDF**: To read PDF documents.
- **LangChain**: For chunking and embeddings.
- **Google Generative AI Embeddings**: For converting text.
- **Faiss**: For storing embeddings in a vector database.
- **Streamlit**: For building the web interface.

### Functions
- **get_pdf_text**: Reads and extracts text from the uploaded PDF.
- **get_text_chunks**: Splits the document into manageable chunks.
- **get_vector**: Converts text chunks into embeddings and stores them.
- **get_conversation_chain**: Generates responses using LLM with the provided context.
- **process_user_question**: Searches relevant documents and generates a response.

### Streamlit UI
- **API Key Input**: Prompts user to input their Google API key.
- **File Uploader**: Allows users to upload PDF documents.
- **Ask Questions**: Interface for querying the document.

## Deployment
### Deploy on Streamlit Community Cloud
1. Create an account on Streamlit.
2. Go to the dashboard and click on "New App".
3. Paste your GitHub URL and deploy.

## Conclusion
We hope this application provides a deeper understanding of how RAG works. Deploy your app on Streamlit Community Cloud to showcase your project. Thank you for watching, and please subscribe for more tutorials.

## Repository

Thank you so much!
