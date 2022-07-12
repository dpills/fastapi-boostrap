from pymongo import MongoClient

from app.config import settings

db = MongoClient(settings.mongo_uri)[settings.mongo_db]
