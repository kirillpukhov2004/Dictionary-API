from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_languages(language_id: int, session: Session):
    languages_translations_query = (
        select(
            models.Language.id.label("language_id"),
            models.Language.word_id,
            models.WordTranslation.translation_id,
        ).join(
            models.WordTranslation,
            models.Language.word_id == models.WordTranslation.word_id,
        )
    ).alias()

    languages_names_query = (
        select(
            languages_translations_query.c.word_id,
            languages_translations_query.c.language_id,
            models.Translation.string,
        )
        .join(
            models.Translation,
            languages_translations_query.c.translation_id == models.Translation.id,
        )
        .where(models.Translation.language_id == language_id)
    )

    return session.execute(languages_names_query).all()


def get_words(language_id: int, session: Session):
    get_words_query = (
        select(
            models.WordTranslation.word_id,
            models.Translation.language_id,
            models.Translation.string,
        )
        .where(models.Translation.language_id == language_id)
        .join(
            models.WordTranslation,
            models.Translation.id == models.WordTranslation.translation_id,
        )
    )

    return session.execute(get_words_query).all()


def create_word(language_id: int, string: str, session: Session):
    new_translation = models.Translation(language_id=language_id, string=string)
    session.add(new_translation)
    session.commit()

    new_word = models.Word()
    session.add(new_word)
    session.commit()

    new_word_translation = models.WordTranslation(
        word_id=new_word.id, translation_id=new_translation.id
    )
    session.add(new_word_translation)
    session.commit()

    return schemas.Word(
        word_id=new_word_translation.word_id,
        language_id=new_translation.language_id,
        string=new_translation.string,
    )


def create_word_translation(
    word_id: int, language_id: int, string: str, session: Session
):
    new_translation = models.Translation(language_id=language_id, string=string)
    session.add(new_translation)
    session.commit()

    new_word_translation = models.WordTranslation(
        word_id=word_id, translation_id=new_translation.id
    )
    session.add(new_word_translation)
    session.commit()

    return schemas.Word(
        word_id=new_word_translation.word_id,
        language_id=new_translation.language_id,
        string=new_translation.string,
    )


def get_word(word_id: int, language_id: int, session: Session):
    get_word_query = (
        select(
            models.WordTranslation.word_id,
            models.Translation.language_id,
            models.Translation.string,
        )
        .where(models.Translation.language_id == language_id)
        .where(models.WordTranslation.word_id == word_id)
        .join(
            models.WordTranslation,
            models.Translation.id == models.WordTranslation.translation_id,
        )
    )

    return session.execute(get_word_query).first()
