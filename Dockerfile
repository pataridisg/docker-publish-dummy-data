FROM python:latest

RUN apt-get update \
    && apt-get upgrade -y

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "publish_dummy_data.py"]
