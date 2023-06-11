from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from . import models


def check_language_id(language_id: int, session: Session) -> bool:
    query = exists(
        select(models.Language).where(models.Language.id == language_id)
    ).select()

    return session.execute(query).scalar()


def check_word_id(word_id: int, session: Session) -> bool:
    query = exists(select(models.Word).where(models.Word.id == word_id)).select()

    return session.execute(query).scalar()


def check_translation(language_id: int, string: str, session: Session) -> bool:
    query = exists(
        select(
            select(models.Translation)
            .where(models.Translation.language_id == language_id)
            .where(models.Translation.string == string)
        )
    )

    return session.execute(query).scalar()
