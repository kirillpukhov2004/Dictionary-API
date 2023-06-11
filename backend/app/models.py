from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from .database import Base


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))

    def __repr__(self):
        return f"Language(id={self.id}, word_id={self.word_id})"


class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    string: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"Translation(id={self.id}, language_id={self.language_id}, string={self.string})"


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)

    translations: Mapped[list[Translation]] = relationship(
        secondary="word_translations"
    )

    def __repr__(self):
        return f"Word(id={self.id})"


class WordTranslation(Base):
    __tablename__ = "word_translations"

    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"), primary_key=True)
    translation_id: Mapped[int] = mapped_column(
        ForeignKey("translations.id"), primary_key=True
    )

    def __repr__(self):
        return f"WordTranslation(word_id={self.word_id}, translation_id={self.translation_id})"
