from main import db

import sqlalchemy as sa

class Word(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)

    def __repr__(self):
        return f"Word(id={self.id})"


class Language(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    word_id = sa.Column(sa.Integer, sa.ForeignKey("word.id"), nullable=False)

    def __repr__(self):
        return f"Language(id={self.id}, word_id={self.word_id})"


class Translation(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    language_id = sa.Column(sa.Integer, sa.ForeignKey("language.id"), nullable=False)
    string = sa.Column(sa.String(255), nullable=False)

    def __repr__(self):
        return f"Translation(id={self.id}, language_id={self.language_id}, string={self.string})"


class WordTranslation(db.Model):
    word_id = sa.Column(sa.Integer, sa.ForeignKey("word.id"), primary_key=True)
    translation_id = sa.Column(sa.Integer, sa.ForeignKey("translation.id"), primary_key=True)

    def __repr__(self):
        return f"WordTranslation(word_id={self.word_id}, translation_id={self.translation_id})"
