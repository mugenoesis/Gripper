FROM python:3.9.5-slim-buster as build
EXPOSE 5000
RUN apt update && apt upgrade -y && pip install --upgrade pip
WORKDIR /gripper
COPY . .
ENTRYPOINT ["/bin/bash", "./setup.sh" ]