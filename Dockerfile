FROM binaryify/netease_cloud_music_api

ENV PYTHONUNBUFFERED=1

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    pip3 install pipenv
WORKDIR /app
COPY mcli.py Pipfile  /app/
RUN pipenv install  --deploy --ignore-pipfile
