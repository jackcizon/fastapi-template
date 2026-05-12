from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from src.core.resources import resources


def get_doc_client() -> AsyncMongoClient:
    return resources.doc_client


def get_doc_db(name: str) -> AsyncDatabase:
    if resources.doc_client is None:
        raise RuntimeError("doc_client is not initialized")
    return resources.doc_client[name]
