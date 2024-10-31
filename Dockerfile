FROM python:3.11.1-slim

WORKDIR /prod

COPY ./requirements.txt /prod/requirements.txt
COPY ./app /prod/app
COPY ./models /prod/models
COPY ./settings.py /prod/settings.py
COPY ./wsgi.py /prod/wsgi.py


RUN pip install --no-cache-dir -r /prod/requirements.txt

# EXPOSE 8000

# CMD ["uvicorn", "wsgi:app", "--host", "0.0.0.0", "--port", "8000"]