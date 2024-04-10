FROM python:3-alpine3.14
WORKDIR /app
RUN apk add gcc python3-dev linux-headers libc-dev libffi libffi-dev --no-cache
RUN pip install poetry==1.7.0
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install
COPY . .
CMD ["sh","-c","poetry run python main.py"]