#!/bin/bash

echo 'Running Server'
if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
  fastapi run src/main.py --host 0.0.0.0 --port 8000
else
  fastapi dev src/main.py --host 0.0.0.0 --port 8000
fi