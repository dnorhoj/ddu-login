FROM python:alpine

WORKDIR /app

COPY Pipfile Pipfile.lock ./
COPY src/ .

# Install pipenv
RUN pip install pipenv gunicorn
RUN pipenv install --system --deploy

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]
