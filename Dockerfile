FROM python:3.8
WORKDIR /workdir

ENV FLASK_APP=flask_augmentations.app:app
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements requirements
COPY src src
COPY setup.py setup.py
RUN pip install -U pip && pip install --no-cache-dir .

EXPOSE 8080

CMD ["flask", "run"]