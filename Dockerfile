
FROM python:3.12

# Set environment variables untuk Poetry
ENV POETRY_VERSION=2.1.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - 

# Tambahkan Poetry ke PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /code

# Copy pyproject.toml dan poetry.lock (lebih efisien untuk caching)
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./alembic.prod.ini /code/alembic.prod.ini

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]