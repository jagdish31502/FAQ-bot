from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

# Function to load model and embeddings
def llm_model():
    try:
        llm = ChatGoogleGenerativeAI(model=os.getenv('GEMINI_MODEL'), verbose=True)
        return llm
    except Exception as e:
        print(f"Error in llm_model: {e}")
        return None