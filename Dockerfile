FROM python:3.12.4-alpine3.20

RUN pip install --no-cache pyyaml PyGithub

WORKDIR /usr/src

COPY src .

ENTRYPOINT [ "python", "/usr/src/main.py" ]