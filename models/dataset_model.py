from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Any
from bson import ObjectId

class Dataset(BaseModel):
    file_path: str
    schema_data: Optional[Any] = None
    stats_json: Optional[Any] = None
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
