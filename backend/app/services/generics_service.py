from app.models.generics import GenericResponse
from typing import List

class GenericsService:
    def __init__(self, db):
        self.db = db

    async def get_generics(self) -> List[GenericResponse]:
        generics = await self.db.generics.find().to_list(None)
        return [GenericResponse(**generic) for generic in generics]