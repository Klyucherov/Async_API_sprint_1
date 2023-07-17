import aioredis
import core.config as conf
import uvicorn
from api.v1 import films, genres, persons
from db import elastic, redis
from elasticsearch import AsyncElasticsearch

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title='Read-only API для онлайн-кинотеатра',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Информация о фильмах, жанрах и людях, участвовавших в создании произведения',
    version='1.0.0'
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (conf.CONNECTION_SETTINGS.redis_host, conf.CONNECTION_SETTINGS.redis_port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(
        hosts=[f'http://{conf.CONNECTION_SETTINGS.elastic_host}:{conf.CONNECTION_SETTINGS.elastic_port}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films')
app.include_router(persons.router, prefix='/api/v1/persons')
app.include_router(genres.router, prefix='/api/v1/genres')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
        reload=True
    )
