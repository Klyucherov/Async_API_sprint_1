from typing import List
from uuid import UUID

from api.v1.models.api_base_model import Base


class PersonBase(Base):
    full_name: str


class PersonFull(PersonBase):
    role: List[str] = []
    film_ids: List[UUID] = []
