#!/user/bin/env bash

source /path/to/your/venv/bin/activate
set -o errexit #exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
