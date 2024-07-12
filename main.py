import os
import json
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize Pinecone
pc = PineconeClient(api_key=pinecone_api_key)

# Define index name and check if it exists
index_name = "travel-destination-index"
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
    with open("destinations.json", "r") as file:
        data = json.load(file)

    # Function to convert destination name and highlights to vector
    def get_vector(destination_name, highlights):
        text = f"Destination: {destination_name}. Highlights: {highlights}"
        return embeddings.embed_query(text)

    # Prepare vectors and metadata
    vectors = []
    for i, item in enumerate(data):
        destination_name = item['destination_name']
        highlights = item['highlights']
        vector = get_vector(destination_name, highlights)
        vectors.append({
            "id": str(i),
            "values": vector,
            "metadata": {"destination_name": destination_name, "highlights": highlights}
        })

    # Upsert vectors to Pinecone with namespace
    namespace = "travel-destination-namespace"
    index.upsert(vectors=vectors, namespace=namespace)

# Helper function to format highlights information
def format_highlights(highlights_str):
    highlights_items = highlights_str.split(', ')
    return '\n'.join(highlights_items)

# Streamlit app
st.title("Travel Destination Recommendation System")
st.write("Enter a destination name below to get highlights information.")

# User input
user_input = st.text_input("Destination Name")

if user_input:
    # Query Pinecone
    query_vector = embeddings.embed_query(user_input)
    results = index.query(vector=query_vector, top_k=1, include_metadata=True, namespace="travel-destination-namespace")

    # Set a similarity threshold
    similarity_threshold = 0.75

    if results['matches'] and results['matches'][0]['score'] > similarity_threshold:
        destination_info = results['matches'][0]['metadata']
        destination_name = destination_info.get('destination_name', 'Unknown destination')
        highlights = destination_info.get('highlights', 'No highlights information found.')

        st.write(f"Destination Name: {destination_name}")
        st.write("Highlights:")
        st.write(format_highlights(highlights))
    else:
        st.write("Destination not found in data")
