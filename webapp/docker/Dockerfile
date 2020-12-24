FROM python:3.7-slim
USER root
WORKDIR /webapp
EXPOSE 80

# TODO post devel remove
RUN apt-get update && apt-get install -y curl less procps
RUN python -m pip install --upgrade pip

RUN mkdir /logs

ADD ./requirements.txt /webapp/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD ./src /webapp/src
ADD ./docker/entrypoint.sh /webapp

CMD ["./entrypoint.sh"]
