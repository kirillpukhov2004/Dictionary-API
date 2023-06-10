from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, utilities, schemas
from .database import SessionLocal

endpoint_base = "/dictionary/api"


app = FastAPI()


def create_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get(endpoint_base)
def get_api_status():
    return "API is up and running"


@app.get(endpoint_base + "/languages", response_model=list[schemas.Word])
def read_languages(language_id: int, session: Session = Depends(create_session)):
    if language_id != 0:
        if not utilities.check_language_id(language_id=language_id, session=session):
            raise HTTPException(
                404, f"Language with language_id={language_id} not found"
            )

    return crud.get_languages(session=session, language_id=language_id)


@app.get(endpoint_base + "/words", response_model=list[schemas.Word])
def read_words(language_id: int, session: Session = Depends(create_session)):
    if not utilities.check_language_id(language_id=language_id, session=session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    return crud.get_words(session=session, language_id=language_id)


@app.post(endpoint_base + "/words", response_model=schemas.Word)
def create_word(word: schemas.WordCreate, session: Session = Depends(create_session)):
    language_id = word.language_id
    if not utilities.check_language_id(language_id=language_id, session=session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    return crud.create_word(
        language_id=language_id, string=word.string, session=session
    )


@app.post(endpoint_base + "/words/{word_id}", response_model=schemas.Word)
def create_word_translation(
    word_id: int, word: schemas.WordCreate, session: Session = Depends(create_session)
):
    if not utilities.check_word_id(word_id=word_id, session=session):
        raise HTTPException(404, f"Word with word_id={word_id} not found")

    language_id = word.language_id
    if not utilities.check_language_id(language_id=language_id, session=session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    return crud.create_word_translation(
        language_id=language_id, string=word.string, session=session
    )


@app.get(endpoint_base + "/words/{word_id}", response_model=schemas.Word)
def read_word(
    word_id: int, language_id: int, session: Session = Depends(create_session)
):
    if not utilities.check_word_id(word_id=word_id, session=session):
        raise HTTPException(404, f"Word with word_id={word_id} not found")

    if not utilities.check_language_id(language_id=language_id, session=session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    return crud.get_word(session=session, word_id=word_id, language_id=language_id)


@app.put(endpoint_base + "/words/{word_id}", response_model=schemas.Word)
def update_word(
    word_id: int, word: schemas.WordUpdate, session: Session = Depends(create_session)
):
    pass


@app.delete(endpoint_base + "/words/{word_id}", response_model=schemas.Word)
def delete_word(
    word_id: int, word: schemas.WordDelete, session: Session = Depends(create_session)
):
    pass
