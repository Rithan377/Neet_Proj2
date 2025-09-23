import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_index")
