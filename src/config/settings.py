import os
from dotenv import load_dotenv
load_dotenv()

GCS_BUCKET=os.getenv("GCS_BUCKET")
PROJECT_ID=os.getenv(("PROJECT_ID"))
REGION="us-central1" 
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_INDEX=os.getenv("PINECONE_INDEX")