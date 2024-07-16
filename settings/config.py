import os
from dotenv import load_dotenv  #Put your token in .env

load_dotenv()

# BOT DISCORD

TOKEN = os.getenv("DS-TOKEN")

# MONGO DB

HOST = os.getenv("MONGO_HOST")
DB_NAME = os.getenv("MONGO_DB_NAME")