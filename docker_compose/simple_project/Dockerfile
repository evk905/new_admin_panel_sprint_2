FROM ython:3.10-slim

WORKDIR /opt/app

ARG USERNAME=myuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'


COPY movies_admin/run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY movies_admin/uwsgi/uwsgi.ini uwsgi.ini

RUN apt update  \
    && apt install -y gcc  \
    && pip install --upgrade pip  \
    && pip install --no-cache-dir -r requirements.txt

COPY movies_admin movies_admin

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 8000
USER myuser

ENTRYPOINT ["./entrypoint.sh"]
