FROM python:2

LABEL "docker_repo"="seldonio"
LABEL "docker_image_name"="testserving"
LABEL "docker_image_version"="0.1"
LABEL "service_type"="MODEL"
LABEL "base_image"="python:2"
LABEL "model_name"="testServing"
LABEL "persistence"="0"
LABEL "api_type"="REST"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY /requirements.txt /tmp/
COPY /seldon_requirements.txt /tmp/
RUN cd /tmp && \
    pip install --no-cache-dir -r seldon_requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir microservice
COPY ./ /microservice/
WORKDIR /microservice

EXPOSE 5000
CMD ["python","-u","microservice.py","testServing","REST","--service-type","MODEL","--persistence","0"]