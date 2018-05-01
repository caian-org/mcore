#!/bin/bash

if [ -e app.db ]; then
    rm app.db
fi

if [ -d migrations ]; then
    rm -rf migrations
fi

migrate_models() {
    printf "\n\n\nMigrating models...\n\n\n"
    flask db init
}

generate_revision() {
    printf "\n\n\nGenerating new revision...\n\n\n"
    flask db migrate
}

upgrade_version() {
    printf "\n\n\nUpgrading to the new version...\n\n\n"
    flask db upgrade
}

migrate_models && generate_revision && upgrade_version
printf "\n\n\n"
