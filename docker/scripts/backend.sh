#!/bin/bash

echo "Applying Migrations"
alembic upgrade head

if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
  echo "Running Server in Production Mode"
  fastapi run src/main.py --host 0.0.0.0 --port 8000
else
  echo "Running Server in Development Mode"
  fastapi dev src/main.py --host 0.0.0.0 --port 8000
fi
