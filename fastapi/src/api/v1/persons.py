from http import HTTPStatus
from typing import List, Optional

from api.v1.models.api_film_models import FilmBase
from api.v1.models.api_person_models import PersonBase, PersonFull
from services.person import PersonService, get_person_service

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get('/search',
            response_model=List[PersonFull],
            summary='Поиск персон',
            description='Поиск по персонам по запросу',
            response_description='Список персон с id, именем и ролью',
            tags=['Персоны']
            )
async def person_search(person_service: PersonService = Depends(get_person_service),
                        page: int = Query(default=1, alias="page_number", ge=1),
                        size: int = Query(default=25, alias="page_size", ge=1, le=100),
                        query: Optional[str] = Query(..., alias='query'),
                        ) -> List[PersonBase]:
    persons = await person_service.search_persons(query=query, page=page, size=size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')

    return [PersonFull(**person.dict()) for person in persons]


@router.get('/{person_id}/film',
            response_model=List[FilmBase],
            summary='Информация о фильмах по персоне',
            description='Данный endpoint предоставляет информацию о фильмах по персоне Id, title, imdb_rating',
            response_description='ID, полное имя, роль',
            tags=['Персоны']
            )
async def films_with_person_details(person_id: str,
                                    person_service: PersonService = Depends(get_person_service)) -> List[FilmBase]:
    films = await person_service.get_films_by_person(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return [FilmBase(**film.dict()) for film in films]


@router.get('/{person_id}',
            response_model=PersonFull,
            summary='Информация о персоне по ID',
            description='Данный endpoint предоставляет полную информацию о персоне по ID',
            response_description='ID, полное имя, роль',
            tags=['Персоны']
            )
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonFull:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return PersonFull(**person.dict())


sort_regex = "^(asc|desc)$"


@router.get('',
            response_model=List[PersonBase],
            summary='Список персон',
            description='Список персон с пагинацией',
            response_description='Список персон с id, названием и рейтингом',
            tags=['Персоны']
            )
async def person_list(person_service: PersonService = Depends(get_person_service),
                      page: int = Query(default=1, alias="page_number", ge=1),
                      size: int = Query(default=25, alias="page_size", ge=1, le=100)
                      ) -> List[PersonBase]:
    persons = await person_service.get_list_persons(page=page, size=size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [PersonBase(**person.dict()) for person in persons]
