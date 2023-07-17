from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from models.models import Film
from services.base_service import BaseDataService

from fastapi import Depends


class FilmService(BaseDataService):
    """
    Класс позволяет взаимодействовать с ElasticSearch и Redis для поиска информации по фильму, включая четкий и
    нечеткий (полнотекстовый) поиск.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index_name = 'movies'

    async def get_list_films(self, page: int, size: int,
                             sort_imdb: str, genre_id: Optional[str]) -> Optional[List[Film]]:
        """
        Метод возвращает все фильмы по параметрам и фильтрации
        :param page: номер страницы
        :param size: количество фильмов на странице
        :param sort_imdb: направление сортировки по рейтингу (по возрастанию asc, по убыванию - desc)
        :param genre_id: ID жанра для фильтрации
        :return: list[Film]
        """

        body = {
            "from": (page - 1) * size,
            "size": size,
            "sort": [{"imdb_rating": {"order": sort_imdb}}]
        }

        if genre_id:
            body["query"] = {
                "nested": {
                    "path": "genres",
                    "query": {
                        "bool": {
                            "must": [{
                                "term": {
                                    "genres.id": {
                                        "value": genre_id
                                    }
                                }
                            }]
                        }
                    }
                }
            }

        return await self._get_data(body, size)

    async def search_films(self, query: str, page: int, size: int) -> Optional[List[Film]]:
        """
        Полнотекстовый поиск по query
        :param query: запрос
        :param page: номер страницы
        :param size: количество фильмов на странице
        :return: list[Film]
        """
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "title^2",
                        "description"
                    ]
                }
            },
            "from": (page - 1) * size,
            "size": size
        }

        return await self._get_data(body, size)


@lru_cache()
def get_film_service(redis: Redis = Depends(get_redis),
                     elastic: AsyncElasticsearch = Depends(get_elastic), ) -> FilmService:

    return FilmService(redis, elastic)
