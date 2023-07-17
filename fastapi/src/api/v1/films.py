from http import HTTPStatus
from typing import List, Optional

from api.v1.models.api_film_models import FilmBase, FilmFull
from services.film import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get('/search',
            response_model=List[FilmBase],
            summary='Поиск фильмов',
            description='Поиск по фильмам по запросу',
            response_description='Список фильмов с id, названием и рейтингом',
            tags=['Фильмы']
            )
async def film_search(film_service: FilmService = Depends(get_film_service),
                      page: int = Query(default=1, alias="page_number", ge=1),
                      size: int = Query(default=25, alias="page_size", ge=1, le=100),
                      query: Optional[str] = Query(..., alias='query'),
                      ) -> List[FilmBase]:
    films = await film_service.search_films(query=query, page=page, size=size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [FilmBase(**film.dict()) for film in films]


@router.get('/{film_id}',
            response_model=FilmFull,
            summary='Информация о фильме по ID',
            description='Данный endpoint предоставляет полную информацию о фильме по ID',
            response_description='ID, название, описание, жанры, рейтинг, список участников кинопроизведения',
            tags=['Фильмы']
            )
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmFull:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmFull(**film.dict())


sort_regex = "^(asc|desc)$"


@router.get('',
            response_model=List[FilmBase],
            summary='Список фильмов',
            description='Список фильмов с пагинацией, фильтрацией по жанрам и сортировкой по году или рейтингу',
            response_description='Список фильмов с id, названием и рейтингом',
            tags=['Фильмы']
            )
async def film_list(film_service: FilmService = Depends(get_film_service),
                    page: int = Query(default=1, alias="page_number", ge=1),
                    size: int = Query(default=25, alias="page_size", ge=1, le=100),
                    sort_imdb: Optional[str] = Query(default='desc', regex=sort_regex, alias='sort_by_rating'),
                    genre_id: Optional[str] = Query(default=None, alias='filter[genre]'),
                    ) -> List[FilmBase]:

    films = await film_service.get_list_films(page=page, size=size, sort_imdb=sort_imdb, genre_id=genre_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [FilmBase(**film.dict()) for film in films]
