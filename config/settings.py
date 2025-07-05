import os
from dotenv import load_dotenv

load_dotenv()

# MAX_CLIENT_UPLOAD_SIZE = int(os.getenv('MAX_CLIENT_UPLOAD_SIZE', 5))
# BACKEND_URL = os.getenv(f'{str(os.getenv('ENV'))}_URL')

class Settings:
    MAX_CLIENT_UPLOAD_SIZE:int = int(os.getenv('MAX_CLIENT_UPLOAD_SIZE', 5))
    BACKEND_URL:str = os.getenv(f'{str(os.getenv('ENV'))}_URL')
    ENV:str = str(os.getenv('ENV'))

settings = Settings()