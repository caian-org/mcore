#!/bin/bash

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

main() {
    if [ -e app.db ]; then
        rm app.db
    fi

    if [ -d migrations ]; then
        rm -rf migrations
    fi

    [[ "$FLASK_APP" != "main.py" ]] && export FLASK_APP=main.py

    migrate_models || exit 1
    generate_revision || exit 1
    upgrade_version || exit 1

    printf "\n\n\n"
}

main
