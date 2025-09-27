from typing import Optional, List, Dict, Any
from bson import ObjectId
from ..core.database import get_database

class DatabaseUtils:
    """Utility functions for database operations."""
    
    @staticmethod
    def convert_object_id(obj: Any) -> Any:
        """Convert ObjectId to string in nested objects."""
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {key: DatabaseUtils.convert_object_id(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [DatabaseUtils.convert_object_id(item) for item in obj]
        return obj
    
    @staticmethod
    async def find_by_id(collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Find a document by its ID."""
        db = await get_database()
        if not db:
            return None
        
        try:
            collection = db[collection_name]
            doc = await collection.find_one({"_id": ObjectId(doc_id)})
            return DatabaseUtils.convert_object_id(doc) if doc else None
        except Exception:
            return None
    
    @staticmethod
    async def find_many(collection_name: str, filter_dict: Dict[str, Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Find multiple documents with optional filtering."""
        db = await get_database()
        if not db:
            return []
        
        collection = db[collection_name]
        cursor = collection.find(filter_dict or {}).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [DatabaseUtils.convert_object_id(doc) for doc in docs]
    
    @staticmethod
    async def insert_one(collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert a single document."""
        db = await get_database()
        if not db:
            return None
        
        collection = db[collection_name]
        result = await collection.insert_one(document)
        return str(result.inserted_id)
    
    @staticmethod
    async def update_one(collection_name: str, doc_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a single document."""
        db = await get_database()
        if not db:
            return False
        
        collection = db[collection_name]
        result = await collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def delete_one(collection_name: str, doc_id: str) -> bool:
        """Delete a single document."""
        db = await get_database()
        if not db:
            return False
        
        collection = db[collection_name]
        result = await collection.delete_one({"_id": ObjectId(doc_id)})
        return result.deleted_count > 0