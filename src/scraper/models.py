from src.common.models import MongoModel


class Article(MongoModel):
    INDEX = {"body": "text", "title": "text"}
