import os
import json
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient, ServerlessSpec

# Set environment variables
os.environ['PINECONE_API_KEY'] = "38ce1c45-3a20-4640-941b-896256951d37"
os.environ['OPENAI_API_KEY'] = "sk-proj-wGHgCJ4COhZNslXtIiLJT3BlbkFJzj9vqNXkS8Qi3GiAvLBD"
 
# Get API keys from environment variables
pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
 
# Initialize Pinecone
pc = PineconeClient(api_key=pinecone_api_key)
 
# Define index name and check if it exists
index_name = "symptoms-remedies-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
 
# Connect to the index
index = pc.Index(index_name)
 
# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=openai_api_key)
 
# Load the JSON data from file and upsert to Pinecone if index is empty
if index.describe_index_stats()['total_vector_count'] == 0:
    with open("C:\Users\Kishor\Desktop\Prompt Engineering\Assignment\RAG\data.json", "r") as file:
        data = json.load(file)
 
    # Function to convert symptom and remedy to vector
    def get_vector(symptom, remedy):
        text = f"Symptom: {symptom}. Remedy: {remedy}"
        return embeddings.embed_documents([text])[0]
 
    # Prepare vectors and metadata
    vectors = []
    for i, item in enumerate(data):
        symptom = item['symptom']
        remedy = item['remedy']
        vector = get_vector(symptom, remedy)
        vectors.append({
            "id": str(i),
            "values": vector,
            "metadata": {"symptom": symptom, "remedy": remedy}
        })
 
    # Upsert vectors to Pinecone with namespace
    namespace = "symptoms-remedies-namespace"
    index.upsert(vectors=vectors, namespace=namespace)
 
# Initialize LangChain components
vectorstore = Pinecone(index=index, embedding=embeddings, text_key='Name', namespace="employee-names-namespace")
 
# Create a retriever
retriever = vectorstore.as_retriever()
 
# ... (keep your existing imports and setup code)
 
# ... (keep your existing imports and setup code)
 
# Streamlit app
st.title("RAG-Based Chatbot for Symptoms and Remedies")
st.write("Enter your symptom below and get a remedy suggestion.")
 
# User input
user_input = st.text_input("Symptom")
 
if user_input:
    # Retrieve documents based on the symptom
    result = retriever.get_relevant_documents(user_input)
 
    # Check if any of the retrieved documents contain relevant information
    found_match = False
    for doc in result:
        if any(symptom.lower() in user_input.lower() for symptom in doc.page_content.split()):
            symptom = doc.page_content
            remedy = doc.metadata.get('remedy', "No remedy found.")
           
            st.write("*Relevant Information:*")
            st.write(f"*Symptom:* {symptom}")
            st.write(f"*Remedy:* {remedy}")
            found_match = True
            break
 
    if not found_match:
        st.write("*Response:* I'm sorry, but I couldn't find any relevant information for that symptom.")