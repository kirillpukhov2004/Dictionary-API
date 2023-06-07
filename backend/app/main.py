endpoint = "/dictionary/api"

# Flask Initialization

from flask import Flask, request, json, jsonify


app = Flask(__name__)

json.provider.DefaultJSONProvider.compact = True
json.provider.DefaultJSONProvider.ensure_ascii = False

# Flask-SQLAlchemy Initialization
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqlconnector://root:0123456789@db:3306/dictionary'

db = SQLAlchemy(app)


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


# Flask-RESTful Initializaiton

from flask_restful import Api, Resource


api = Api(app)


class WordResource(Resource):
    def post(self):
        post_json = request.get_json()

        language_id = post_json.get("language_id")
        if language_id == None:
            return "", 404
        
        check_language_id_query = db.exists(db.select(Language).where(Language.id == language_id)).select()
        if not db.session.execute(check_language_id_query).scalar():
            return "", 404
        

        string = post_json.get("string")
        if string == None or type(string) is not str:
            return "", 404
        
        new_translation = Translation(language_id=language_id, string=string)
        db.session.add(new_translation)

        word_id = post_json.get("word_id")
        if  word_id == None:
            new_word = Word()
            db.session.add(new_word)
            db.session.commit()

            new_word_translation = WordTranslation(word_id=new_word.id, translation_id=new_translation.id)
            db.session.add(new_word_translation)
            db.session.commit()

            response_dict = {
                "word_id": new_word_translation.word_id,
                "language_id": new_translation.language_id,
                "string": new_translation.string
            }
            return "", 200
        else: 
            check_word_id_query = db.exists(db.select(Word).where(Word.id == word_id)).select()

            if not db.session.execute(check_word_id_query).scalar():
                return "", 404

            new_word_translation = WordTranslation(word_id=word_id, translation_id=new_translation.id)
            db.session.add(new_word_translation)
            db.session.commit()

            response_dict = {
                "word_id": new_word_translation.word_id,
                "language_id": new_translation.language_id,
                "string": new_translation.string
            }
            return "", 200


class WordsResource(Resource):
    def get(self): 
        # Getting parameters
        language = request.args.get("language", type=str)
        if language == None:
            return "", 404

        # Getting language_id for specified language
        language_id = get_language_id(language)
        if language_id == None:
            return "", 404
        
        translations_query = (
            db.select(WordTranslation.word_id.label("word_id"), Translation.string)
            .where(Translation.language_id == language_id)
            .join(WordTranslation, Translation.id == WordTranslation.translation_id)
        )

        words = db.session.execute(translations_query).tuples()

        response_dict = {
            "items": [{"id": t[0], "string": t[1]} for t in words]
        }
        return jsonify(response_dict)


class LanguagesResoruce(Resource):
    def get(self):
        # Getting arguments
        language = request.args.get("language", type=str)
        if language == None or language == "":
            language = "English"

        # Getting language_id for specified language
        language_id = get_language_id(language)
        if language_id == None:
            return "", 404

        # Getting languages names in specified language
        languages_translations_query = (
            db.select(Language.id.label("language_id"), Language.word_id, WordTranslation.translation_id,)
            .join(WordTranslation, Language.word_id == WordTranslation.word_id)
        ).alias()
        languages_names_query = (
            db.select(languages_translations_query.c.language_id, Translation.string.label("name"))
            .join(Translation, languages_translations_query.c.translation_id == Translation.id)
            .where(Translation.language_id == language_id)
        )
        languages_names = db.session.execute(languages_names_query).tuples()

        response_dict = {
            "items": [{"id": language_name[0], "string": language_name[1]} for language_name in languages_names]
        }
        return jsonify(response_dict)
    
    
api.add_resource(WordResource, endpoint + "/word")
api.add_resource(WordsResource, endpoint + "/words")
api.add_resource(LanguagesResoruce, endpoint + "/languages")


# Helper Functions

@app.get(endpoint)
def api_check():
    return "API is working"

def get_language_id(language: str):
    languages_translations_query = (
        db.select(Language.id.label("language_id"), Language.word_id, WordTranslation.translation_id)
        .join(WordTranslation, Language.word_id == WordTranslation.word_id)
    )
    languages_names_query = (
        db.select(languages_translations_query.c.language_id, Translation.language_id.label("translation_language_id"), Translation.string.label("name"))
        .join(Translation, languages_translations_query.c.translation_id == Translation.id)
    )
    language_id_query = (
        db.select(languages_names_query.c.language_id)
        .where(languages_names_query.c.name == language)
    )
    try:
        language_id = db.session.execute(language_id_query).scalars().one()
        return language_id
    except:
        return None
