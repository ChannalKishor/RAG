import os
import json
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient, ServerlessSpec

# Set environment variables
os.environ['PINECONE_API_KEY'] = "38ce1c45-3a20-4640-941b-896256951d37"
os.environ['OPENAI_API_KEY'] = "sk-proj-YXJivLFmrIw2MVf9aJzMT3BlbkFJQ6bxWcdv49KRtqUB7Qwq"
 
# Get API keys from environment variables
pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
 
# Initialize Pinecone
pc = PineconeClient(api_key=pinecone_api_key)
 
# Define index name and check if it exists
index_name = "employee-names-index"
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
    with open("C:\\Users\\Kishor\\Desktop\\Prompt Engineering\\Assignment\\RAG\\data.json", "r") as file:
        data = json.load(file)
 
    # Function to convert employee attributes to vector
    def get_vector(employee):
        text = f"Name: {employee['Name']}, Age: {employee['Age']}, Salary: {employee['Salary']}, Gender: {employee['Gender']}, Department: {employee['Department']}"
        return embeddings.embed_documents([text])[0]
 
    # Prepare vectors and metadata
    vectors = []
    for i, item in enumerate(data):
        vector = get_vector(item)
        vectors.append({
            "id": str(i),
            "values": vector,
            "metadata": item
        })
 
    # Upsert vectors to Pinecone with namespace
    namespace = "employee-namespace"
    index.upsert(vectors=vectors, namespace=namespace)
 
# Initialize LangChain components
vectorstore = Pinecone(index=index, embedding=embeddings, text_key='Name', namespace="employee-namespace")
 
# Create a retriever
retriever = vectorstore.as_retriever()
 
# Streamlit app
st.title("Employee Information Retrieval")
st.write("Enter an attribute to find relevant employee information.")
 
# User input
user_input = st.text_input("Enter Name, Age, Salary, Gender, or Department")
 
if user_input:
    # Retrieve documents based on the input attribute
    result = retriever.get_relevant_documents(user_input)
 
    # Check if any of the retrieved documents contain relevant information
    found_match = False
    for doc in result:
        employee_info = doc.metadata
        st.write("Relevant Employee Information:")
        st.write(f"Name: {employee_info['Name']}")
        st.write(f"Age: {employee_info['Age']}")
        st.write(f"Salary: {employee_info['Salary']}")
        st.write(f"Gender: {employee_info['Gender']}")
        st.write(f"Department: {employee_info['Department']}")
        found_match = True
        break
 
    if not found_match:
        st.write("Response: I'm sorry, but I couldn't find any relevant employee information for that attribute.")