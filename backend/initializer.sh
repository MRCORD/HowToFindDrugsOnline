#!/bin/bash


echo "Current working directory:"
pwd


echo "Contents of /backend directory:"
ls -l /backend


# Start the application using gunicorn on port 8000
exec gunicorn -b 0.0.0.0:8000 app.main:app -w 2 -k uvicorn.workers.UvicornWorker
#exec uvicorn app.main:app --host 0.0.0.0 --port 8000