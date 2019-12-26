#
# Memento
# Backend
# Dockefile
#

FROM python:3.7-alpine as develop

# setup nonroot user to drop root permissions
RUN addgroup -S user && adduser -S user -G user
RUN mkdir /backend && chown user /backend 
RUN mkdir /scripts && chown user /scripts 
ENV HOME=/backend/
WORKDIR /backend

# install packages & pip packages
COPY src/backend/requirements.txt /backend/
ENV PATH=/backend/.local/bin:$PATH
RUN apk add --no-cache postgresql-libs bash && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# configure API version
ARG API_VERSION=0
ENV API_VERSION=$API_VERSION

# copy container scripts
ENV PATH=/scripts:$PATH
COPY containers/backend /scripts
RUN chmod u+x -R /scripts

# copy project source code
COPY src/backend /backend/

# set backend container entrypoint
EXPOSE 5000
ENV FLASK_APP=app.py
ENTRYPOINT [ "/scripts/entrypoint.sh" ]
CMD python run.py
