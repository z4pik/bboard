FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /usr/src/bboard
COPY requirements.txt /usr/src/requirements.txt

RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/bboard

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]