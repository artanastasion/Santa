FROM python:latest
RUN mkdir /usr/src/SantaBot
WORKDIR /usr/src/SantaBot
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/SantaBot
CMD ["python", "bot.py"]
