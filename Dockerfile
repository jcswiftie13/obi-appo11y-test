FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY pgtest.py /app/pgtest.py

ENV PYTHONUNBUFFERED=1

CMD ["python3", "/app/pgtest.py"]