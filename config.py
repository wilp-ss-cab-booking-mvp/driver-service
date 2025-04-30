import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
JWT_SECRET = os.getenv("JWT_SECRET", "default-secret")
BOOKING_SERVICE_URL = os.getenv("BOOKING_SERVICE_URL")
