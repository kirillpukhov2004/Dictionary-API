from pydantic import BaseModel


class Word(BaseModel):
    word_id: int
    language_id: int
    string: str

    class Config:
        orm_mode = True


class WordRead(BaseModel):
    language_id: int


class WordCreate(BaseModel):
    language_id: int
    string: str


class WordUpdate(BaseModel):
    language_id: int
    string: str


class WordDelete(BaseModel):
    language_id: int


class LanguageRead(BaseModel):
    language_id: int
