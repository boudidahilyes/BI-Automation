from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from services.ingestion_service import IngestionService
from repositories.dataset_repository import DatasetRepository
from db.mongo_connection import get_db

router = APIRouter()

db = get_db()
dataset_repo = DatasetRepository(db)
ingestion_service = IngestionService(dataset_repo)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", summary="Upload dataset and infer schema")
async def upload_dataset(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        dataset_id = ingestion_service.save_file_and_profile(file_path)
        return {"dataset_id": dataset_id, "message": "Dataset uploaded and profiled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
