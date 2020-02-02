#
# Memento
# Backend
# Dockefile
#

FROM python:3.7-alpine AS base

# setup nonroot user to drop root permissions
RUN addgroup -S user && adduser -S user -G user
RUN mkdir /backend && chown user /backend 
RUN mkdir /scripts && chown user /scripts 
ENV HOME=/backend/
WORKDIR /backend

# install packages & pip packages
COPY src/backend/requirements.txt /backend/
ENV PATH=/backend/.local/bin:$PATH
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# configure envrionment variable sessions
ARG API_VERSION=0
ENV API_VERSION=$API_VERSION

# copy container scripts
ENV PATH=/scripts:$PATH
COPY containers/backend /scripts
RUN chmod u+x -R /scripts

# configure backend container entrypoint
EXPOSE 5000
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENTRYPOINT [ "/scripts/entrypoint.sh" ]

## develop image
FROM base AS develop
# install development tools
RUN apk add --no-cache entr the_silver_searcher
# copy project source code
COPY src/backend /backend
# develop container comand
CMD ["ag", "-g", "''", "|", "entr", "-r", "python", "run.py"]

## production image
FROM base AS production
# copy project source code
COPY src/backend /backend
# production container comand
CMD ["python","run.py"]
