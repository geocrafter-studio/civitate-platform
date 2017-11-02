#!/bin/bash

# Export environment variables
export $(cat /platform/src/.env | xargs)
# Collect static
python src/manage.py collectstatic --noinput
# Compile translations
cd /platform/src/flavors/${FLAVOR}
python /platform/src/manage.py compilemessages
# Start app in production mode
npm run start-prod
