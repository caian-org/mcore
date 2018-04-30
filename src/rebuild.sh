#!/bin/bash

rm app.db
rm -rf migrations

flask db init
flask db migrate
flask db upgrade
