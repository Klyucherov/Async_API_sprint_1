from functools import lru_cache
from typing import List, Optional

from redis.asyncio import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from models.models import Genre
from services.base_service import BaseDataService

from fastapi import Depends


class GenreService(BaseDataService):
    """
    Класс позволяет взаимодействовать с ElasticSearch и Redis для поиска информации по жанру, включая четкий и
    нечеткий (полнотекстовый) поиск.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index_name = 'genres'
        self.service_name = 'GenreService'

    async def get_list_genres(self, page: int, size: int) -> Optional[List[Genre]]:
        """
        Метод возвращает все жанры
        :param page: номер страницы
        :param size: количество фильмов на странице
        :return: list[Genre]
        """

        body = {
            "from": (page - 1) * size,
            "size": size,
            "sort": [{
              "name.raw": {
                "order": "asc"
              }
            }]
        }

        return await self._get_data(body, size)


@lru_cache()
def get_genre_service(redis: Redis = Depends(get_redis),
                      elastic: AsyncElasticsearch = Depends(get_elastic), ) -> GenreService:

    return GenreService(redis, elastic)
