FROM python:3.13.0rc1-alpine3.20

RUN pip install --no-cache pyyaml PyGithub

WORKDIR /usr/src

COPY src .

ENTRYPOINT [ "python", "/usr/src/main.py" ]