FROM python:3.11

WORKDIR /app

RUN pip install rasa-pro
RUN pip install google-generativeai

COPY . .

CMD [ "rasa","run", "--enable-api" ]