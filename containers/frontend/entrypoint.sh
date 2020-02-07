#!/bin/sh
#
# Memento
# Frontend 
# Container Entrypoint
#

# wait for the api backend  to become available
echo
if wait-for $BACKEND_API_HOST -t 30
then 
    # run command
    ash -c "$*"
fi
