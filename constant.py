import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Credentials
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")

# Secret Key for JWT
SECRET_KEY = os.getenv("SECRET_KEY")

# MongoDB Connection URI
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DB}"
