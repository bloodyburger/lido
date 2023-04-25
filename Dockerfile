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
COPY .env /lido
#COPY . /lido

EXPOSE 8000
CMD ["sh", "runserver.sh"]