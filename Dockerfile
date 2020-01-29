FROM python:3.7
LABEL maintainer "Ole Christian Astrup <ole.christian.astrup@dnvgl.com>"
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]