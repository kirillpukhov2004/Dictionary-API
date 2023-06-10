from sqlalchemy import Column, ForeignKey, Integer, String

from .database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Word(id={self.id})"


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("word.id"), nullable=False)

    def __repr__(self):
        return f"Language(id={self.id}, word_id={self.word_id})"


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language_id = Column(Integer, ForeignKey("language.id"), nullable=False)
    string = Column(String(255), nullable=False)

    def __repr__(self):
        return f"Translation(id={self.id}, language_id={self.language_id}, string={self.string})"


class WordTranslation(Base):
    __tablename__ = "word_translations"

    word_id = Column(Integer, ForeignKey("word.id"), primary_key=True)
    translation_id = Column(Integer, ForeignKey("translation.id"), primary_key=True)

    def __repr__(self):
        return f"WordTranslation(word_id={self.word_id}, translation_id={self.translation_id})"
