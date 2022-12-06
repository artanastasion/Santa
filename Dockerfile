FROM python:latest
WORKDIR /SantaBot
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]