#
# Memento
# Frontend Container
# Dockerfile
#

# base image
FROM node:12.2.0-alpine AS base

# setup nonroot user to drop root permissions
RUN addgroup -S user && adduser -S user -G user
RUN mkdir /frontend && chown user /frontend 
RUN mkdir /scripts && chown user /scripts 
ENV HOME=/frontend/
WORKDIR /frontend

# install packages
COPY src/frontend/package-lock.json /frontend
COPY src/frontend/package.json /frontend
RUN yarn install && yarn global add react-scripts@3.0.1 

# copy container scripts
ENV PATH=/scripts:$PATH
COPY containers/frontend /scripts
RUN chmod u+x -R /scripts

# configure frontend container 
EXPOSE 3000
ARG REACT_APP_BACKEND_API_HOST=memento.mrzzy.co
ENV REACT_APP_BACKEND_API_HOST=${REACT_APP_BACKEND_API_HOST}
ARG REACT_APP_BACKEND_API_PROTOCOL_INSECURE=
ENV REACT_APP_BACKEND_API_PROTOCOL_INSECURE=${REACT_APP_BACKEND_API_PROTOCOL_INSECURE}

ENTRYPOINT [ "/scripts/entrypoint.sh" ]

## develop
FROM base AS develop
# copy project source code
COPY src/frontend /frontend
ENV REACT_APP_BACKEND_API_HOST=localhost:5000
ENV REACT_APP_BACKEND_API_PROTOCOL_INSECURE=1
CMD ["yarn", "start"]

FROM develop AS production

# serve production build
RUN yarn global add serve
ENV REACT_APP_BACKEND_API_HOST=memento.mrzzy.co
ENV REACT_APP_BACKEND_API_PROTOCOL_INSECURE=
RUN yarn build && mv build /build

CMD ["serve", "-l", "tcp://0.0.0.0:3000", "/build"]
