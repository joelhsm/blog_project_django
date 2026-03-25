#!/bin/sh

database_verify.sh
collectstatic.sh
migrate.sh
# tailwind.sh
runserver.sh