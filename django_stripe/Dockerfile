FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD gunicorn djangostripe.wsgi:application --bind 0.0.0.0:8081
