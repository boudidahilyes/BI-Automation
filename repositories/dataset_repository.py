from typing import Optional

from bson import ObjectId

from models.dataset_model import Dataset

class DatasetRepository:
    def __init__(self, db):
        self.collection = db["datasets"]

    def save(self, dataset: Dataset) -> str:
        data = dataset.dict()
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get_by_id(self, id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": ObjectId(id)})

    def update_schema(self, id: str, schema_json: dict):
        self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"schema_json": schema_json}}
        )

    def update_stats(self, id: str, stats_json: dict):
        self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"stats_json": stats_json}}
        )

    def list(self):
        return list(self.collection.find())
