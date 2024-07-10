from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize HuggingFace embeddings
def embedding_model():
    try:
        embeddings = HuggingFaceEmbeddings(model_name=os.getenv('EMBED_MODEL'))
        # print(embeddings)
        return  embeddings
    except Exception as e:
        print(f"Error in embedding_model: {e}")
        return None