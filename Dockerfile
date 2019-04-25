FROM python:3.6

ENV GITHUB_OAUTH_KEY d057c87657c4fa14177386f905a5207bfa2b649c

COPY . /verloop/
WORKDIR /verloop/

RUN mkdir /var/log/uwsgi/

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install -r requirements.txt
# --src /usr/local/src

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]