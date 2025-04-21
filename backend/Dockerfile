FROM python:latest

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

COPY ./requirements-test.txt /backend/requirements-test.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements-test.txt

COPY ./app /backend/app

COPY ./scripts /backend/scripts

COPY entrypoint.sh /backend/

WORKDIR /backend/app

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
