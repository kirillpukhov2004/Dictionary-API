from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, utilities, schemas
from .database import SessionLocal

endpoint_base = "/dictionary/api"


app = FastAPI(docs_url="/dictionary/api/docs", redoc_url="/dictionary/api/redoc")


def create_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get(endpoint_base + "/languages", response_model=list[schemas.Word])
def read_languages(language_id: int, session: Session = Depends(create_session)):
    if language_id != 0:
        if not utilities.check_language_id(language_id, session):
            raise HTTPException(
                404, f"Language with language_id={language_id} not found"
            )

    return crud.read_languages_trnslations(language_id, session)


@app.get(endpoint_base + "/words", response_model=list[schemas.Word])
def read_words(language_id: int, session: Session = Depends(create_session)):
    if not utilities.check_language_id(language_id, session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    return crud.read_words_translations(language_id, session)


@app.post(endpoint_base + "/words", response_model=schemas.Word)
def create_word(word: schemas.WordCreate, session: Session = Depends(create_session)):
    if not utilities.check_language_id(word.language_id, session):
        raise HTTPException(
            404, f"Language with language_id={word.language_id} not found"
        )

    return crud.create_word(word.language_id, word.string, session)


@app.post(endpoint_base + "/words/{word_id}", response_model=schemas.Word)
def create_word_translation(
    word_id: int, word: schemas.WordCreate, session: Session = Depends(create_session)
):
    if not utilities.check_word_id(word_id, session):
        raise HTTPException(404, f"Word with word_id={word_id} not found")

    if not utilities.check_language_id(word.language_id, session):
        raise HTTPException(
            404, f"Language with language_id={word.language_id} not found"
        )

    return crud.create_word_translation(word.language_id, word.string, session)


@app.get(endpoint_base + "/words/{word_id}", response_model=schemas.Word)
def read_word(
    word_id: int, language_id: int, session: Session = Depends(create_session)
):
    if not utilities.check_word_id(word_id, session):
        raise HTTPException(404, f"Word with word_id={word_id} not found")

    if not utilities.check_language_id(language_id=language_id, session=session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    return crud.read_word(word_id, language_id, session)


@app.put(endpoint_base + "/words/{word_id}")
def update_word(
    word_id: int,
    language_id: int,
    word: schemas.WordUpdate,
    session: Session = Depends(create_session),
):
    if not utilities.check_word_id(word_id, session):
        raise HTTPException(404, f"Word with word_id={word_id} not found")

    if not utilities.check_language_id(language_id=language_id, session=session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    crud.update_word_translation(word_id, language_id, word.string)


@app.delete(endpoint_base + "/words/{word_id}")
def delete_word(
    word_id: int, language_id: int, session: Session = Depends(create_session)
):
    if not utilities.check_word_id(word_id=word_id, session=session):
        raise HTTPException(404, f"Word with word_id={word_id} not found")

    if not utilities.check_language_id(language_id=language_id, session=session):
        raise HTTPException(404, f"Language with language_id={language_id} not found")

    crud.delete_word_translation(word_id, language_id, session)
