#! /bin/bash

cd /home/${USER}/3.2-crud
git pull origin main
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
sudo systemctl restart gunicorn
