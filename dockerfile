FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV HOME=/app
ENV APP_HOME=/app/web

RUN mkdir -p $APP_HOME && mkdir -p build/static
WORKDIR $APP_HOME

RUN apt-get -y update \
    && apt-get install -y \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./
RUN pip install -r requirements.txt psycopg2==2.9.3

COPY . .

RUN python3 manage.py collectstatic -c --noinput \
    && chmod 777 $APP_HOME

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--worker-tmp-dir" ,"/dev/shm"]
CMD ["CCL_Library.wsgi", "-b", "0.0.0.0:8000"]
