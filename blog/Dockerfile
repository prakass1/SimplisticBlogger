FROM python:3.7.9-slim
RUN apt-get update && apt-get install -y gcc && apt-get install -y default-libmysqlclient-dev

COPY SimplisticBlogger/blog /app/blog
COPY SimplisticBlogger/requirements.txt /app/blog
COPY SimplisticBlogger/common /app/common
COPY SimplisticBlogger/instance /app/instance
COPY SimplisticBlogger/.env /app/blog
WORKDIR /app/blog

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD flask run --host ${FLASK_HOST} --port ${FLASK_BLOG_PORT}

#CMD ["flask", "run", "--port ${FLASK_BLOG_PORT}"]
