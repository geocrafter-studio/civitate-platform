# Run the python tests
src/manage.py test base
STATUS=$?
if [ $STATUS -ne 0 ]
then exit $STATUS
fi
