
FROM python:3.12


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./alembic.prod.ini /code/alembic.prod.ini


CMD ["fastapi", "run", "app/main.py", "--port", "80"]