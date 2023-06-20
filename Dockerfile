FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

COPY . /app/

# Use daphne or asgiref to run the application
CMD ["daphne", "config.asgi:application", "-b", "0.0.0.0", "-p", "8000"]