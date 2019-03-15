#########################################
## Dockerfile for the dev-tools project.
##
## This dockerfile should be used for development purposes.
##
#########################################

FROM alpine

ADD . /dev-tools
WORKDIR /dev-tools

# Run python as: python3, and pip as: pip3
RUN apk add bash python3 python3-dev gcc musl-dev
RUN pip3 install --upgrade pip
RUN pip3 install -U setuptools