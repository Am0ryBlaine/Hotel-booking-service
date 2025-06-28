FROM python:3.13

RUN apt-get update && \
    apt-get install -y locales libpq-dev gcc && \
    sed -i '/en_US.UTF-8/s/^# //' /etc/locale.gen && \
    locale-gen

RUN pip install poetry psycopg2-binary

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN poetry install --no-interaction --no-ansi

CMD ["python", "dhotelservice/manage.py", "runserver", "0.0.0.0:8000", "--settings=hotel_service.settings"]



