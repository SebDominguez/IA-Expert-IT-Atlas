#! /bin/bash

alembic revision --autogenerate -m "add_caf_enfants_columns"

# then run
# alembic upgrade head