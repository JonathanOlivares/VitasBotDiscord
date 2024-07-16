FROM python:3.10.13

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

RUN apt update && apt upgrade -y && apt-get install -y ffmpeg

COPY .. /app

RUN rm requirements.txt

CMD ["python", "bot.py"]