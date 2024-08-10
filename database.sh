#!/bin/bash

sudo -i -u postgres psql < scripts/deletedb.sql
sudo -i -u postgres psql < scripts/createdb.sql
python adopet_backend/manage.py migrate
sudo -i -u postgres psql adopetbd < scripts/state.sql
sudo -i -u postgres psql adopetbd < scripts/city.sql
sudo -i -u postgres psql adopetbd < scripts/address.sql
sudo -i -u postgres psql adopetbd < scripts/user.sql
sudo -i -u postgres psql adopetbd < scripts/user_metadata.sql
sudo -i -u postgres psql adopetbd < scripts/animal.sql
sudo -i -u postgres psql adopetbd < scripts/animalimage.sql
