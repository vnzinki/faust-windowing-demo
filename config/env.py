import os

from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)
KAFKA_URI = os.getenv('KAFKA_URI')
