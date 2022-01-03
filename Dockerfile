FROM python:3.8.3

RUN mkdir /code
WORKDIR /code
COPY . /code

RUN pip install redis datetime pymongo requests beautifulsoup4
CMD ["python", "main.py"]

