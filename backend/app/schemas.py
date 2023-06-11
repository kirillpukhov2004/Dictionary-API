from pydantic import BaseModel


class Word(BaseModel):
    word_id: int
    language_id: int
    string: str

    class Config:
        orm_mode = True


class WordCreate(BaseModel):
    language_id: int
    string: str


class WordUpdate(BaseModel):
    string: str


class LanguageRead(BaseModel):
    language_id: int
