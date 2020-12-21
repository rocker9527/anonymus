FROM python:3.8-alpine3.12

LABEL maintainer="Trait Code"

# set the working directory in the container
RUN mkdir /Code
WORKDIR /Code

# install dependencies
RUN apk add --no-cache --virtual .build-deps gcc libffi-dev musl-dev openssl-dev \
    && pip install --no-cache-dir python-telegram-bot \
    && apk del .build-deps gcc libffi-dev musl-dev openssl-dev

# copy source code
COPY src/ .

# command to run on container start
CMD [ "python", "./main.py" ]