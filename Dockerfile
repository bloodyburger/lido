FROM python:3.9

RUN mkdir /lido
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
WORKDIR /lido

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY . /lido
RUN pip install -r requirements.txt

ENV SNOWFLAKE_USER=nothing
ENV SNOWFLAKE_PASSWORD=nothing
ENV SNOWFLAKE_ACCOUNT=nothing
ENV SNOWFLAKE_WAREHOUSE=nothing
ENV SNOWFLAKE_DATABASE=nothing
ENV SNOWFLAKE_SCHEMA=nothing
ENV DJANGO_SECRET=mysecretkey

RUN apt-get update && apt install nano -y
#RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]