#Builds your image, installs dependencies
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

#Waits for DB, then starts Flask
CMD ["sh", "-c", "python wait_for_db.py && python app.py"]
