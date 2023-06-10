from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from . import models


def check_language_id(language_id: int, session: Session) -> bool:
    check_language_id_query = exists(
        select(models.Language).where(models.Language.id == language_id)
    ).select()

    return session.execute(check_language_id_query).scalar()


def check_word_id(word_id: int, session: Session) -> bool:
    check_word_id_query = exists(
        select(models.Word).where(models.Word.id == word_id)
    ).select()

    return session.execute(check_word_id_query).scalar()
