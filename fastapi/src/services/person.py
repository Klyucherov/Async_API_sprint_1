import logging
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from models.models import Film, Person
from services.base_service import BaseDataService

from fastapi import Depends

PERSON_FILM = 50


class PersonService(BaseDataService):
    """
    Класс позволяет взаимодействовать с ElasticSearch и Redis для поиска информации по персоне, включая четкий и
    нечеткий (полнотекстовый) поиск.
    """

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index_name = 'persons'
        self.service_name = 'PersonService'

    async def get_list_persons(self, page: int, size: int) -> Optional[List[Person]]:
        """
        Метод возвращает все персоны по параметрам и фильтрации
        :param page: номер страницы
        :param size: количество персон на странице
        :return: list[Person]
        """

        body = {
            "from": (page - 1) * size,
            "size": size,
            "sort": [{
              "full_name.raw": {
                "order": "desc"
              }
            }]
        }

        return await self._get_data(body, size)

    async def search_persons(self, query: str, page: int, size: int) -> Optional[List[Person]]:
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
                        "full_name"
                    ]
                }
            },
            "from": (page - 1) * size,
            "size": size
        }

        return await self._get_data(body, size)

    async def get_films_by_person(self, person_id: str) -> Optional[List[Film]]:

        multi_field_query = [{
            "nested": {
                "path": role,
                "query": {
                    "bool": {
                        "must": [{
                            "term": {
                                f"{role}.id": {
                                    "value": person_id
                                }
                            }
                        }]
                    }
                }
            }
        } for role in ('actors', 'writers', 'directors')]

        body = {
            "query": {
                "bool": {
                    "should": multi_field_query
                }
            }
        }

        logging.info(body)

        return await self._get_data(body=body, index_name='movies', size=PERSON_FILM)


@lru_cache()
def get_person_service(redis: Redis = Depends(get_redis),
                       elastic: AsyncElasticsearch = Depends(get_elastic), ) -> PersonService:
    return PersonService(redis, elastic)
