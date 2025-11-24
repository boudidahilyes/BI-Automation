import pandas as pd
from datetime import datetime
from repositories.dataset_repository import DatasetRepository
from models.dataset_model import Dataset

class IngestionService:
    def __init__(self, repo: DatasetRepository):
        self.repo = repo

    def save_file_and_profile(self, file_path: str) -> str:
        # Read file
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type")

        # Infer schema
        schema = {}
        for col in df.columns:
            dtype = str(df[col].dtype)
            schema[col] = dtype

        # Basic stats
        stats = {}
        for col in df.columns:
            stats[col] = {
                "unique": int(df[col].nunique()),
                "missing": int(df[col].isnull().sum()),
                "min": float(df[col].min()) if pd.api.types.is_numeric_dtype(df[col]) else None,
                "max": float(df[col].max()) if pd.api.types.is_numeric_dtype(df[col]) else None,
                "mean": float(df[col].mean()) if pd.api.types.is_numeric_dtype(df[col]) else None,
            }

        # Create dataset object
        dataset = Dataset(
            file_path=file_path,
            schema_data=schema,
            stats_json=stats,
        )

        # Save to DB
        dataset_id = self.repo.save(dataset)
        return dataset_id
