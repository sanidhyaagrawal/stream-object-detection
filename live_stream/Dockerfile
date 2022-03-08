FROM ubuntu:latest

RUN apt-get update
RUN apt install -y python3-pip zip htop screen libgl1-mesa-glx
RUN alias python=python3
# RUN pip install --upgrade pip setuptools wheel
# RUN apk update && apk add build-base libzmq musl-dev python3 python3-dev zeromq-dev
# RUN apk update && apk add build-base libzmq musl-dev python3 python3-dev zeromq-dev
# RUN apk add py-pip
COPY requirements.txt ./

RUN python3 -m pip install --no-cache -r requirements.txt

COPY . ./

ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=prod
EXPOSE 5555
ENTRYPOINT ["python3", "server.py"]
