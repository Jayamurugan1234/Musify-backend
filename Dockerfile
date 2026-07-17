FROM python:3.14

WORKDIR /app

# copy requirements first (important for caching)
COPY requirements.txt .

# install dependencies inside container
RUN pip install --no-cache-dir -r requirements.txt

# copy full project
COPY . .

# run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]