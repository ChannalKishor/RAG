# RAG Chatbot for Tourism Recommendations

This repository contains the code for a Retrieval-Augmented Generation (RAG) chatbot that provides information and highlights for various travel destinations. The chatbot uses OpenAI embeddings and Pinecone for vector storage and similarity search.

## Features

- Retrieves and displays highlights for a given travel destination.
- Uses Pinecone for vector storage and similarity search.
- Utilizes OpenAI embeddings to convert destination names and highlights into vectors.
- Interactive user interface built with Streamlit.

## Requirements

- Python 3.8+
- Streamlit
- Pinecone
- LangChain
- OpenAI
- dotenv

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/tourism-rag-chatbot.git
    cd tourism-rag-chatbot
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Pinecone and OpenAI API keys:
    ```env
    PINECONE_API_KEY=your-pinecone-api-key
    OPENAI_API_KEY=your-openai-api-key
    ```

4. Ensure you have a JSON file named `destinations.json` in the root directory containing the travel destination data. The file should follow this structure:
    ```json
    [
      {
        "destination_name": "Paris",
        "highlights": "Eiffel Tower, Louvre Museum, Notre-Dame Cathedral"
      },
      {
        "destination_name": "New York",
        "highlights": "Statue of Liberty, Central Park, Times Square"
      }
    ]
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Enter a destination name in the input field to get the highlights information.

## Code Explanation

- **Load Environment Variables**: Loads API keys from the `.env` file.
- **Initialize Pinecone**: Sets up the Pinecone client and checks if the specified index exists, creating it if necessary.
- **Load Data and Upsert to Pinecone**: Reads the destination data from a JSON file, converts it into vectors using OpenAI embeddings, and upserts it to Pinecone if the index is empty.
- **Streamlit App**: Creates a simple web interface where users can input a destination name to get the corresponding highlights.

## Future Enhancements

- Add more detailed information for each destination.
- Implement more robust error handling.
- Enhance the user interface with additional features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
