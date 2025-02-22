FROM python:3.9.21

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "ML_API:app", "--host", "0.0.0.0", "--port", "8000"]
