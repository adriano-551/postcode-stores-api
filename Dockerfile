FROM tiangolo/uwsgi-nginx-flask:python3.11

ENV STATIC_URL=/static
ENV STATIC_PATH=/store-postcodes-api/api/static

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt
