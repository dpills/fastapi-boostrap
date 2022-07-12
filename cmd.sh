#!/bin/bash

if [ $1 == "format" ]
then
    poetry run python -m isort --multi-line 3 --trailing-comma --line-length 79 app
    poetry run python -m flake8 --max-line-length=79 app
    poetry run python -m black --line-length=79 app
elif [ $1 == "test" ]
then
    poetry run python -m coverage run --source ./app -m pytest --disable-warnings
elif [ $1 == "start" ]
then
    poetry run python -m app.main
else
   echo "unknown command $1"
fi
