FROM python:3.6.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalação das dependências do sistema operacional
RUN apt-get update && \
    apt-get install -y python3-dev libffi-dev gcc musl-dev libssl-dev curl nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install Django
RUN pip3 install djangorestframework
RUN pip3 install gunicorn

COPY script.py .


COPY . .

COPY ./entrypoint.sh /


ENTRYPOINT ["sh", "/entrypoint.sh"]

