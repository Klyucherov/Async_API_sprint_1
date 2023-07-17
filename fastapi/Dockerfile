FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV HOME=/home/app
ENV APP_HOME=/home/app/fastapi

WORKDIR $APP_HOME

COPY ./requirements.txt .
COPY ./entrypoint.sh .

RUN pip install --upgrade pip &&  \
    pip install --no-cache-dir -r requirements.txt

COPY src/ .

RUN groupadd -r app &&  \
    useradd -d $HOME -r -g app app && \
    chown app:app -R $HOME

RUN chmod +x  $APP_HOME/entrypoint.sh

EXPOSE 8001

USER app

ENTRYPOINT ["/home/app/fastapi/entrypoint.sh"]
