from datetime import datetime
from typing import Dict, Union
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
from uuid import uuid4
from models import Show


## DAL Encapsulates all the data access logic for the application
class ShowDAL:
    def __init__(self, show_collection: AsyncIOMotorCollection):
        self._show_collection = show_collection

    async def list_shows(self, session=None):
        print(self._show_collection)
        async for doc in self._show_collection.find(
            {},
            session=session,
        ):
            yield Show.from_doc(doc)

    async def create_show(self, name: str, session=None) -> str:
        response = await self._show_collection.insert_one(
            {"name": name, "items": []},
            session=session,
        )
        return str(response.inserted_id)

    async def get_show(self, id: Union[str, ObjectId], session=None) -> Show:
        doc = await self._show_collection.find_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return Show.from_doc(doc)

    async def delete_show(self, id: Union[str, ObjectId], session=None) -> bool:
        response = await self._show_collection.delete_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return response.deleted_count == 1

    async def create_show(
        self,
        id: Union[str, ObjectId],
        label: str,
        session=None,
    ) -> Union[str, None]:
        result = await self._show_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {
                "$push": {
                    "items": {
                        "id": uuid4().hex,
                        "label": label,
                        "checked": False,
                    }
                }
            },
            session=session,
            return_document=ReturnDocument.AFTER,
        )
        if result:
            return Show.from_doc(result)

    async def update_show(
            self,
            show_id: Union[str, ObjectId],
            updates: Dict[str, Union[str, datetime, bool, list]],
            session=None
        ) -> Union[Show, None]:
            """Update a show with given updates.

            Args:
                show_id: The ID of the show to update.
                updates: A dictionary of the fields to update.
                session: Optional session object for transaction support.

            Returns:
                The updated Show object, or None if no show was found.
            """
            # Convert show_id to ObjectId if it's not already
            show_id = ObjectId(show_id) if not isinstance(show_id, ObjectId) else show_id
            
            # Use $set to update only the specified fields
            result = await self._show_collection.find_one_and_update(
                {"_id": show_id},
                {"$set": updates},
                session=session,
                return_document=ReturnDocument.AFTER,
            )
            
            if result:
                return Show.from_doc(result)
            return None
    
    async def delete_show(
        self,
        doc_id: Union[str, ObjectId],
        item_id: str,
        session=None,
    ) -> Union[str, None]:
        result = await self._show_collection.find_one_and_update(
            {"_id": ObjectId(doc_id)},
            {"$pull": {"items": {"id": item_id}}},
            session=session,
            return_document=ReturnDocument.AFTER,
        )
        if result:
            return Show.from_doc(result)