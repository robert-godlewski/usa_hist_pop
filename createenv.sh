#!/bin/bash
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
python3 createdb.py
deactivate