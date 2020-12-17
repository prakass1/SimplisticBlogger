FROM python:3.7.9-slim

COPY . /app/blog
COPY ./requirements.txt /app/blog
COPY ./common /app/common
COPY ./instance /app/instance

WORKDIR /app/blog

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD flask run --host ${FLASK_HOST} --port ${FLASK_BLOG_PORT}

#CMD ["flask", "run", "--port ${FLASK_BLOG_PORT}"]
