#! /bin/bash

if [ "$(id -u)" != "0" ]
then
dep_sh="#! /bin/bash

cd /home/${USER}/3.2-crud
git pull origin main
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
sudo systemctl restart gunicorn"
echo "$dep_sh" | tee /home/${USER}/3.2-crud/deploy.sh > /dev/null

dep_exp="#! /bin/bash/expect

spawn /home/${USER}/3.2-crud/deploy.sh
expect "password"
send -- "1\r"
expect eof"
echo "$dep_exp" | tee /home/${USER}/3.2-crud/deploy.sh > /dev/null

sudo chmod +x /home/${USER}/3.2-crud/deploy.sh
sudo chmod +x /home/${USER}/3.2-crud/deploy.exp

else
clear
echo "****************************************"
echo "----------------------------------------"
echo "Вы не должны быть root, файлы не созданы"
echo "----------------------------------------"
echo "****************************************"
fi
