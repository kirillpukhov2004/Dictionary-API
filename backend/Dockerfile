FROM python:3.10-alpine

RUN pip install Flask Flask-SQLAlchemy Flask-RESTful mysql-connector-python

ENV FLASK_APP "/app/main.py"
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8000

ENV FLASK_DEBUG True

EXPOSE 8000

CMD ["flask", "run"]
