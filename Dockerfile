FROM python:3.14

WORKDIR /app

# copy requirements first (important for caching)
COPY requirements.txt .

# install dependencies inside container
RUN pip install --no-cache-dir -r requirements.txt

# copy full project
COPY . .

# collect static files, run migrations, then start gunicorn
CMD python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput && \
    gunicorn config.wsgi:application --bind 0.0.0.0:$PORT