FROM amd64/python:3.8
WORKDIR /workdir

ENV FLASK_APP=flask_augmentations.app:app
ENV FLASK_RUN_HOST=0.0.0.0

COPY flask_augmentations ./flask_augmentations
COPY mymodel ./mymodel

RUN pip install -U pip \
    && pip install --no-cache-dir ./mymodel \
    && pip install --no-cache-dir ./flask_augmentations

EXPOSE 8080
CMD ["flask", "run", "-p", "8080"]