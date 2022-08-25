FROM tiangolo/uvicorn-gunicorn-fastapi

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY /src/app /src/app
WORKDIR /src/app


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]