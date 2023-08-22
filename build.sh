#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migramigrat


python manage.py createsuperuser --noinput