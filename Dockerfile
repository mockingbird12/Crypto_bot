FROM python:3

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN ["pip3", "install", "pytelegrambotapi", "--upgrade"]

COPY . .

#CMD ["python", "./main.py"]
CMD ["python", "./crypto_parser.py"]