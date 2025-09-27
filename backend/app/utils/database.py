
from typing import Dict, List, Optional, Any
from bson import ObjectId
from ..core.database import get_database

class DatabaseUtils:
    """Database utility functions for CRUD operations"""
    
    @staticmethod
    async def create(collection_name: str, document: Dict[str, Any]):
        """Create a new document"""
        db = await get_database()
        if db is None:
            raise Exception("Database not available")
        
        collection = db[collection_name]
        result = await collection.insert_one(document)
        return result
    
    @staticmethod
    async def find_by_id(collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """Find document by ID"""
        db = await get_database()
        if db is None:
            return None
        
        try:
            collection = db[collection_name]
            document = await collection.find_one({"_id": ObjectId(document_id)})
            if document:
                document["id"] = str(document["_id"])
            return document
        except Exception:
            return None
    
    @staticmethod
    async def find_one(collection_name: str, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one document by filter"""
        db = await get_database()
        if db is None:
            return None
        
        collection = db[collection_name]
        document = await collection.find_one(filter_dict)
        if document:
            document["id"] = str(document["_id"])
        return document
    
    @staticmethod
    async def find_many(
        collection_name: str, 
        filter_dict: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        db = await get_database()
        if db is None:
            return []
        
        collection = db[collection_name]
        if filter_dict is None:
            filter_dict = {}
        
        cursor = collection.find(filter_dict).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        for doc in documents:
            doc["id"] = str(doc["_id"])
        
        return documents
    
    @staticmethod
    async def update_by_id(
        collection_name: str, 
        document_id: str, 
        update_dict: Dict[str, Any]
    ):
        """Update document by ID"""
        db = await get_database()
        if db is None:
            raise Exception("Database not available")
        
        collection = db[collection_name]
        result = await collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": update_dict}
        )
        return result
    
    @staticmethod
    async def delete_by_id(collection_name: str, document_id: str):
        """Delete document by ID"""
        db = await get_database()
        if db is None:
            raise Exception("Database not available")
        
        collection = db[collection_name]
        result = await collection.delete_one({"_id": ObjectId(document_id)})
        return result
    
    @staticmethod
    async def count_documents(
        collection_name: str, 
        filter_dict: Dict[str, Any] = None
    ) -> int:
        """Count documents in collection"""
        db = await get_database()
        if db is None:
            return 0
        
        collection = db[collection_name]
        if filter_dict is None:
            filter_dict = {}
        
        count = await collection.count_documents(filter_dict)
        return count
    
    @staticmethod
    async def aggregate(collection_name: str, pipeline: List[Dict[str, Any]]):
        """Perform aggregation query"""
        db = await get_database()
        if db is None:
            return []
        
        collection = db[collection_name]
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return results
