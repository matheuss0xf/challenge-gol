import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL is None:
        raise ValueError('DATABASE_URL environment variable is missing')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
