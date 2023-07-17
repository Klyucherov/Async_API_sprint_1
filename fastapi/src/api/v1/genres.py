from http import HTTPStatus
from typing import List

from api.v1.models.api_genre_models import GenreBase
from services.genre import GenreService, get_genre_service

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


sort_regex = "^(asc|desc)$"


@router.get('/{genre_id}',
            response_model=GenreBase,
            summary='Информация о жанре',
            description='Данный endpoint предоставляет информацию о жанре',
            response_description='ID, название жанра',
            tags=['Жанры']
            )
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> GenreBase:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return GenreBase(**genre.dict())


@router.get('',
            response_model=List[GenreBase],
            summary='Список жанров',
            description='Список жанров с пагинацией',
            response_description='Список жанров с id и названием',
            tags=['Жанры']
            )
async def film_list(film_service: GenreService = Depends(get_genre_service),
                    page: int = Query(default=1, alias="page_number", ge=1),
                    size: int = Query(default=25, alias="page_size", ge=1, le=100)) -> List[GenreBase]:
    genres = await film_service.get_list_genres(page=page, size=size)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')

    return [GenreBase(**genre.dict()) for genre in genres]
