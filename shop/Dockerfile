FROM python:3

WORKDIR /app

USER root
ENV PYTHONUNBUFFERED 1

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ARG ENV
ARG CONFIG

RUN python3 -m pip install --upgrade pip
RUN pip3 install pipenv

COPY ./shop/Pipfile .
COPY ./shop/Pipfile.lock .
RUN if [ "$ENV" = "dev" ]; then \
    pipenv install --dev --deploy --clear --system --ignore-pipfile; \
else \
    pipenv install --deploy --clear --system --ignore-pipfile; \
fi


COPY ./shop .
RUN chmod +x /app/docker-entrypoint.sh
ENV ENV=$ENV
RUN export DJANGO_SETTINGS_MODULE=admin.settings
ENTRYPOINT ["/app/docker-entrypoint.sh"]