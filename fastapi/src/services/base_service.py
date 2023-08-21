import logging
from typing import List, Optional

from redis.asyncio import Redis
from api.v1.models.api_film_models import FilmFull
from api.v1.models.api_genre_models import GenreBase
from api.v1.models.api_person_models import PersonFull
from elasticsearch import AsyncElasticsearch, NotFoundError
from models.models import Film, Person, Genre

MODELS = {
    "movies": Film,
    "persons": Person,
    "genres": Genre
}

CACHE_EXPIRE_IN_SECONDS = 60 * 5


class BaseDataService:
    """
    Класс представляет базовый интерфейс для работы с ElasticSearch и Redis. Получение по id (или прочему ключу)
    документов и их кеширование.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index_name: str = '', service_name: str = 'base'):
        self.redis = redis
        self.elastic = elastic
        self.index_name = index_name
        self.service_name = service_name

    async def get_by_id(self, doc_id: str) -> FilmFull | PersonFull | GenreBase | None:
        """
        Возвращает документ по ключу (id). Ищет документ по ключу doc_id в кэше Redis и,
        если не находит, обращается к ElasticSearch. Возвращает None при отсутствии в Elastic.

        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: экземпляр модели данных self.model (FilmFull | PersonFull | GenreBase) или None
        """
        data = await self._get_item_from_cache(doc_id)
        if not data:
            data = await self._get_item_from_elastic(doc_id)
            if not data:
                return None
            await self._put_item_to_cache(data)

        else:
            data = MODELS[self.index_name].parse_raw(data)
        return data

    async def _get_item_from_cache(self, doc_id: str) -> FilmFull | PersonFull | GenreBase | None:
        """
        Ищет документ по ключу doc_id в кэше Redis
        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: FilmFull | PersonFull | GenreBase | None
        """
        if self.redis.exists(doc_id):
            logging.info('[%s] from cache by id', self.service_name)
            return await self.redis.get(f'{self.index_name}{doc_id}')

    async def _put_item_to_cache(self, doc: FilmFull | PersonFull | GenreBase) -> None:
        """
        Сохраняет документ в кэш Redis.
        :param doc: экземпляр модели данных FilmFull | PersonFull | GenreBase
        :return: None
        """
        logging.info('[%s] write to cache by id', self.service_name)
        await self.redis.set(f'{self.index_name}{doc.id}', doc.json(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def _get_item_from_elastic(self, doc_id: str) -> FilmFull | PersonFull | GenreBase | None:
        """

        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: FilmFull | PersonFull | GenreBase | None
        """
        try:
            doc = await self.elastic.get(index=self.index_name, id=doc_id)
            logging.info('[%s] from elastic by id', self.service_name)

            result = MODELS[self.index_name](**doc['_source'])
        except NotFoundError:
            logging.info('[%s] can\'t find in elastic by id', self.service_name)
            return None
        return result

    async def _get_full_data_from_cache(self, key: str, redis_range: int) -> Optional[list]:
        """
        Метод предназначен для получения массива (списка) данных из кэша
        :param key: ключ, по которому требуеся достать данные из кэша
        :param redis_range:
        :return: Optional[list]
        """
        data = await self.redis.lrange(key, 0, redis_range)
        return data

    async def _put_full_data_to_cache(self, data: list, key: str):
        """
        Метод сохраняет в кэш массив (список) данных по ключу key.
        :param data:
        :param key:
        :return:
        """
        logging.info('[%s] write film_data to cache', self.service_name)
        await self.redis.rpush(key, *data)

    @staticmethod
    def _get_hash(kwargs):
        return str(hash(kwargs))

    async def _get_data(self, body: dict, size: int,
                        index_name: str = None) -> List[FilmFull | PersonFull | GenreBase] | None:
        """
        Метод достает данные из кэша или эластика
        :param body: тело запроса
        :param size: количество записей
        :param index_name: имя индекса
        :param model: модель для парсинга возвращаемого результата
        :return:
        """

        if not index_name:
            index_name = self.index_name

        redis_key = self._get_hash(f'{str(body)}{index_name}')

        data = await self._get_full_data_from_cache(key=redis_key, redis_range=size)

        if not data:

            data = await self._get_data_from_elastic(body=body, index=index_name)

            if not data:
                return None

            cache_data = [item.json() for item in data]

            await self._put_full_data_to_cache(data=cache_data, key=redis_key)

        else:
            data = [MODELS[self.index_name].parse_raw(item) for item in data]
            logging.info('[%s] data from cache', self.service_name)

        return data

    async def _get_data_from_elastic(self, body: dict, index: str) -> List[FilmFull | PersonFull | GenreBase] | None:
        """
        Возвращает список данных из кэша или Elastic
        :param body: тело запроса к elasticsearch
        :return: List[FilmFull | PersonFull | GenreBase] | None
        """

        try:
            data = await self.elastic.search(index=index, body=body)
            data = [MODELS[self.index_name](**item['_source']) for item in data['hits']['hits']]

            logging.info('[%s] get data from elastic', self.service_name)
        except NotFoundError:
            logging.info("[%s] can't find data in elastic", self.service_name)
            return None

        return data
