FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install libgl1 -y

RUN pip install -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]

