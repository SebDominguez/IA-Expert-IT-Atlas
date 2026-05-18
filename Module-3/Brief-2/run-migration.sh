#! /bin/bash

# first run :
#alembic init alembic

# edit files

# then run:
# alembic revision --autogenerate -m "ajout_colonnes_enfants_et_caf"
# then run
# alembic upgrade head
# check script in alambic/version

# check db:
# docker exec -it postgres psql -U python -d db -c "\d finance"
# docker exec -it postgres psql -U python -d db -c "\d users"