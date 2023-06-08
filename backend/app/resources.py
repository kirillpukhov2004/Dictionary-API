from flask import request, jsonify

from flask_restful import Resource

from main import db

import models as m

class Word(Resource):
    def post(self):
        post_json = request.get_json()

        language_id = post_json.get("language_id")
        if language_id == None:
            return "", 404
        
        check_language_id_query = db.exists(db.select(m.Language).where(m.Language.id == language_id)).select()
        if not db.session.execute(check_language_id_query).scalar():
            return "", 404
        

        string = post_json.get("string")
        if string == None or type(string) is not str:
            return "", 404
        
        new_translation = m.Translation(language_id=language_id, string=string)
        db.session.add(new_translation)

        word_id = post_json.get("word_id")
        if  word_id == None:
            new_word = m.Word()
            db.session.add(new_word)
            db.session.commit()

            new_word_translation = m.WordTranslation(word_id=new_word.id, translation_id=new_translation.id)
            db.session.add(new_word_translation)
            db.session.commit()

            response_dict = {
                "word_id": new_word_translation.word_id,
                "language_id": new_translation.language_id,
                "string": new_translation.string
            }
            return "", 200
        else: 
            check_word_id_query = db.exists(db.select(m.Word).where(m.Word.id == word_id)).select()

            if not db.session.execute(check_word_id_query).scalar():
                return "", 404

            new_word_translation = m.WordTranslation(word_id=word_id, translation_id=new_translation.id)
            db.session.add(new_word_translation)
            db.session.commit()

            response_dict = {
                "word_id": new_word_translation.word_id,
                "language_id": new_translation.language_id,
                "string": new_translation.string
            }
            return "", 200


class Words(Resource):
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
            db.select(m.WordTranslation.word_id.label("word_id"), m.Translation.string)
            .where(m.Translation.language_id == language_id)
            .join(m.WordTranslation, m.Translation.id == m.WordTranslation.translation_id)
        )

        words = db.session.execute(translations_query).tuples()

        response_dict = {
            "items": [{"id": t[0], "string": t[1]} for t in words]
        }
        return jsonify(response_dict)


class Languages(Resource):
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
            db.select(m.Language.id.label("language_id"), m.Language.word_id, m.WordTranslation.translation_id,)
            .join(m.WordTranslation, m.Language.word_id == m.WordTranslation.word_id)
        ).alias()
        languages_names_query = (
            db.select(languages_translations_query.c.language_id, m.Translation.string.label("name"))
            .join(m.Translation, languages_translations_query.c.translation_id == m.Translation.id)
            .where(m.Translation.language_id == language_id)
        )
        languages_names = db.session.execute(languages_names_query).tuples()

        response_dict = {
            "items": [{"id": language_name[0], "string": language_name[1]} for language_name in languages_names]
        }
        return jsonify(response_dict)


def get_language_id(language: str):
    languages_translations_query = (
        db.select(m.Language.id.label("language_id"), m.Language.word_id, m.WordTranslation.translation_id)
        .join(m.WordTranslation, m.Language.word_id == m.WordTranslation.word_id)
    )
    languages_names_query = (
        db.select(languages_translations_query.c.language_id, m.Translation.language_id.label("translation_language_id"), m.Translation.string.label("name"))
        .join(m.Translation, languages_translations_query.c.translation_id == m.Translation.id)
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