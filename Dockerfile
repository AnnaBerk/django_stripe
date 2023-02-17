FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "djangostripe.wsgi:application", "--bind", "0:8000" ]