FROM python:3.9.5-slim-buster as build
RUN apt update && apt upgrade -y && apt install python3-pip -y
WORKDIR /gripper
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]