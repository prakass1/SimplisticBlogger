FROM python:3.7.9-slim
RUN apt-get update && apt-get install -y gcc && apt-get install -y default-libmysqlclient-dev

COPY SimplisticBlogger/blog_admin /app/blog_admin
COPY SimplisticBlogger/requirements.txt /app/blog_admin
COPY SimplisticBlogger/common /app/common
COPY SimplisticBlogger/instance /app/instance
COPY SimplisticBlogger/.env /app/blog_admin
WORKDIR /app/blog_admin

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD flask run --host ${FLASK_HOST} --port ${FLASK_ADMIN_PORT}
#CMD ["flask", "run", "--port ${FLASK_ADMIN_PORT}"]
