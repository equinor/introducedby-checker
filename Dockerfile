FROM python:3.10.13-alpine3.18

RUN pip install --no-cache pyyaml PyGithub

WORKDIR /usr/src

COPY src .

ENTRYPOINT [ "python", "/usr/src/main.py" ]