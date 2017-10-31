#!/bin/bash

npm install
npm run build
python src/manage.py collectstatic --noinput
python src/manage.py compilemessages
npm run start-prod
#gunicorn wsgi:application -w 3 -b 0.0.0.0:${PORT} --log-level=debug
