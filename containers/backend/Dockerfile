#
# Memento
# Backend API
# Dockefile
#

FROM python:3.7-alpine as develop

# setup nonroot user to drop root permissions
RUN addgroup -S user && adduser -S user -G user
RUN mkdir /backend && chown user /backend 
ENV HOME=/backend/
WORKDIR /backend

# install pip modules
ENV PATH=/backend/.local/bin:$PATH
COPY requirements.txt /backend/
RUN pip install --user -r requirements.txt

# configure API version
ARG API_VERSION=0
ENV API_VERSION=$API_VERSION

# copy project source code
COPY . /backend/

# run db migrations
RUN flask db upgrade

# set backend container entrypoint
EXPOSE 5000
ENV FLASK_APP=app.py
CMD flask run --host=0.0.0.0 # listen on all addresses
