from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
import json

# Function to load PDF and store into chromadb
def insert_into_chromadb(file_path, embeddings):
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")

    except Exception as e:
        print(f"Error in load_data: {e}")
        return None
    
# Function for load data from chromadb
def load_data(embeddings, file_path):
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    filter_criteria = {"source": {"$in": [file_path]}}
    retriever = db.as_retriever(search_kwargs={'filter': filter_criteria})
    return retriever

# Function to generate response using prompt template
def prompt_template(llm, retriever, question):
    try:
        template = '''
                    JSON FORMAT: 
                    You are a FAQ bot. Use only the ### context ### provided to accurately answer in *JSON FORMAT* of user's ### question ###. The question includes a query regarding product details provided in the context.
                    Instructions:
                    1. Ensure the response is not blank.
                    2. Provide the response strictly in *JSON FORMAT* without additional information.
                    3. Base your answer solely on the given context.
                    4. Take a look at the given examples and give me output in the same format.

                    Context:
                    {context}

                    Question:
                    {question}

                    *JSON FORMAT*
                    {{
                        "product_category": "category of the product (e.g., food, electronics)",
                        "product_name": "name of the product",
                        "answer" : "answer of the provided question"                              
                    }}

                    <examples>
                    {{
                        "product_category": "food",
                        "product_name": "aloe berry nectar",
                        "answer": "90.7%"
                    }}
                    {{
                        "product_category": "food",
                        "product_name": "aloe peaches",
                        "answer": "Consume 8 fl. oz. daily. Pour over ice or mix with fruit juice, and enjoy the delightful taste of nature's bounty any time of the day"
                    }}
                    {{
                        "product_category": "skin care",
                        "product_name": "hydrating face cream",
                        "answer": "suitable for all skin types"}}
                    }}
                    </examples>   
                '''
        prompt = ChatPromptTemplate.from_template(template)
        
        chain = (
            {"context": retriever , "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        question = json.dumps(question)
        response = chain.invoke(question)
        try:
            response_json = json.loads(response)
            return response_json, None
        except json.JSONDecodeError:
            return None, response
    
    except Exception as e:
        print(f"Error in prompt_template: {e}")
        return None