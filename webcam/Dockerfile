# FROM python:3.8.5

# WORKDIR /usr/app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libopencv-dev \
#     python3-opencv \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# COPY requirements.txt ./
# RUN pip install --upgrade pip
# RUN pip install --no-cache -r requirements.txt

# COPY . ./

# ENV PYTHONUNBUFFERED=1
# ENV PYTHON_ENV=prod

# ENTRYPOINT ["python3", "app.py"]

FROM ubuntu:latest

RUN apt update && apt install -y python3-pip zip htop screen libgl1-mesa-glx
RUN alias python=python3

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt


ADD . /app


ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

ENTRYPOINT ["python3", "app.py"]