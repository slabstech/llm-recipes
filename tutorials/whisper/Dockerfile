FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install git ffmpeg -y --no-install-recommends
RUN pip3 install   -r requirements.txt \
 && pip3 install  "git+https://github.com/openai/whisper.git" 

COPY app.py /app

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
