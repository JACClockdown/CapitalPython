FROM python:3-slim-buster

WORKDIR /code

COPY ./ /code

COPY ./requirements.txt /code

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
