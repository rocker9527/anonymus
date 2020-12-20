FROM python:3.8-slim

LABEL maintainer="Trait Code"

# set the working directory in the container
RUN mkdir /Code
WORKDIR /Code

# install dependencies
RUN pip install --no-cache-dir python-telegram-bot

# copy source code
COPY src/ .

# command to run on container start
CMD [ "python", "./main.py" ]