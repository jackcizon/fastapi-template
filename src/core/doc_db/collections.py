from pymongo.asynchronous.database import AsyncDatabase


class MongoCollections:
    def __init__(self, doc_db: AsyncDatabase):
        self.doc_db = doc_db

    # @property
    # def collection_name(self):
    #     return self.doc_db.get_collection("name")
