FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apk add bash --update-cache --repository https://pkgs.alpinelinux.org/package/edge/main/ --allow-untrusted
CMD PYTHONPATH=. python main/main.py