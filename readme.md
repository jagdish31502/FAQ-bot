# FAQ Bot for Product Details 

This project implements a FAQ bot using Flask, Gemini model, LangChain, ChromaDB, and PostgreSQL to handle product details PDFs and provide answers to FAQs extracted from the PDFs.

## Features
Product PDF Upload: Upload product's PDF.
FAQ Endpoint: API endpoint to ask questions and retrieve answers from the uploaded PDFs.
Database Integration: Uses PostgreSQL to store questions, answers, and file paths.
Gemini Model: Utilizes the Gemini model for getting answers.
LangChain: Facilitates document processing and retrieval tasks.
ChromaDB: Backend storage for document metadata and embeddings.
PostgreSQL : Storing questions and its answers.

# env:
.env file contains:
        UPLOAD_FOLDER = 'path where you want to store your product pdfs'

        #LLM Model
        GEMINI_MODEL = 'gemini-pro'
        GOOGLE_API_KEY = "google api key for using gemini model"

        #Embedding model
        EMBED_MODEL = 'all-MiniLM-L6-v2'

        #PostgreSQL connectivity credentials
        USER = "postgres username"
        PASSWORD = "password"
        HOST = "localhost"
        PORT = "5432"
        DATABASE_NAME = "your database name"
        TABLE_NAME = "your table name"



APIs
1. /product_pdf
Upload a product PDF to extract FAQs. The bot processes the PDF and stores relevant data in PostgreSQL.

Request
Method: POST
Body: Multipart form-data with key = file, type= file, and value= PDF.
Response
Status: 200 OK
Content: JSON response confirming successful upload.

2. /faq
Ask a question to retrieve an answer from the stored PDFs.

Request
Method: POST
Body: JSON with question parameter containing the question text. ex. "question" : "your question".
Response
Status: 200 OK
Content: JSON response with the answer to the question.


## Installation

To run the project locally, follow these steps:

Clone the repository:
git clone https://github.com/jagdish31502/FAQ-bot.git

cd faq-bot

Install dependencies:

pip install -r requirements.txt

create .env file.

Set up PostgreSQL database.

Run Flask application:
flask run



