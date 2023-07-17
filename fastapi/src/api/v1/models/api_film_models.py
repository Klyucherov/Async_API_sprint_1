from datetime import date
from typing import List, Optional

from api.v1.models.api_base_model import Base
from api.v1.models.api_genre_models import GenreBase
from api.v1.models.api_person_models import PersonBase


class FilmBase(Base):
    id: str
    title: str
    imdb_rating: Optional[float]


class FilmFull(FilmBase):
    description: str = None
    creation_date: date = None
    genres: List[GenreBase] = []
    actors: List[PersonBase] = []
    directors: List[PersonBase] = []
    writers: List[PersonBase] = []
