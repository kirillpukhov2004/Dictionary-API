from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from . import models, schemas, utilities


def read_languages_trnslations(language_id: int, session: Session):
    query = (
        select(
            models.Word.id.label("word_id"),
            models.Translation.language_id.label("language_id"),
            models.Translation.string.label("string"),
        )
        .join(models.Word.translations)
        .where(models.Word.id.in_(select(models.Language.word_id)))
        .where(models.Translation.language_id == language_id)
    )

    return session.execute(query).all()


def create_word(language_id: int, string: str, session: Session):
    translation: models.Translation
    if not utilities.check_translation(language_id, string, session):
        translation = models.Translation(language_id=language_id, string=string)
        session.add(translation)
        session.commit()
    else:
        query = (
            select(models.Translation)
            .where(models.Translation.language_id == language_id)
            .where(models.Translation.string == string)
        )
        translation = session.execute(query).scalar()

    word = models.Word()
    session.add(word)
    session.commit()

    word.translations.append(translation)
    session.commit()

    return schemas.Word(
        word_id=word.id,
        language_id=translation.language_id,
        string=translation.string,
    )


def create_word_translation(
    word_id: int, language_id: int, string: str, session: Session
):
    translation: models.Translation
    if not utilities.check_translation(language_id, string, session):
        translation = models.Translation(language_id=language_id, string=string)
        session.add(translation)
        session.commit()
    else:
        query = (
            select(models.Translation)
            .where(models.Translation.language_id == language_id)
            .where(models.Translation.string == string)
        )
        translation = session.execute(query).scalar()

    word_translation = models.WordTranslation(
        word_id=word_id, translation_id=translation.id
    )
    session.add(word_translation)
    session.commit()

    return schemas.Word(
        word_id=word_id,
        language_id=translation.language_id,
        string=translation.string,
    )


def read_words_translations(language_id: int, session: Session):
    query = (
        select(
            models.Word.id.label("word_id"),
            models.Translation.language_id.label("language_id"),
            models.Translation.string.label("string"),
        )
        .join(models.Word.translations)
        .where(models.Translation.language_id == language_id)
    )

    return session.execute(query).all()


def read_word_translation(word_id: int, language_id: int, session: Session):
    query = (
        select(
            models.Word.id.label("word_id"),
            models.Translation.language_id.label("language_id"),
            models.Translation.string.label("string"),
        )
        .join(models.Word.translations)
        .where(models.Word.id == word_id)
        .where(models.Translation.language_id == language_id)
    )

    return session.execute(query).first()


def update_word_translation(
    word_id: int, language_id: int, string: str, session: Session
):
    word_translation_id = (
        select(models.Translation.id)
        .join(models.Word.translations)
        .where(models.Word.id == word_id)
        .where(models.Translation.language_id == language_id)
        .as_scalar()
    )

    query = (
        update(models.Translation)
        .values({"string": string})
        .where(models.Translation.id == word_translation_id)
    )

    session.execute(query)


def delete_word_translation(word_id: int, language_id: int, session: Session):
    word_translation_id = (
        select(models.Translation.id)
        .join(models.Word.translations)
        .where(models.Word.id == word_id)
        .where(models.Translation.language_id == language_id)
        .as_scalar()
    )

    query = delete(models.Translation).where(
        models.Translation.id == word_translation_id
    )

    session.execute(query)
