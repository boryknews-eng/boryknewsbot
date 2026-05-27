import os
from dotenv import load_dotenv

load_dotenv()  # <-- читає .env файл

TOKEN = os.getenv("8898513998:AAG2cnBH11bzp4hG2vupguOdRa58UlzDegQ")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
