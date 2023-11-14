#! /bin/bash

IP=$(ip a | awk 'BEGIN{ "hostname -I | cut -d\" \" -f 1" | getline ip} $2 ~ ip {print $2}' | cut -d / -f 1)

if [ "$(id -u)" != "0" ]
    then
        CONFIG_env="SECRET_KEY=PCEJRFkjn985FC3887Y87h*&lpef095ik
            DEBUG=True
            ALLOWED_HOSTS=${IP}
            DB_ENGINE=django.db.backends.postgresql
            DB_NAME=ci_cd
            DB_USER=postgres
            DB_PASSWORD=123456
            DB_HOST=localhost
            DB_PORT=5432"
        echo "$CONFIG_env" | tee /home/${USER}/ci_cd/.env && echo [ create .env ]

        CONFIG_project="server {
            listen 80;  # nginx обычно работает на 80 порту, его и слушаем
            server_name ${IP};
            location /static/ {  # где искать файлы проекта - в папке проекта будет искаться папка static и файлы будут браться из нее
                root /home/${USER}/ci_cd/;
            }
            location / {  # Все остальные запросы будут проксироваться в сокет
            include proxy_params;
            proxy_pass http://unix:/home/${USER}/ci_cd/stocks_products/project.sock;
            }
        }"
        echo "$CONFIG_project" | sudo tee /etc/nginx/sites-available/project && echo [ create project ]

        CONFIG_gunicorn_service="[Unit]
            Description=Gunicorn service
            After=network.target

            [Service]
            User=${USER}
            Group=www-data
            WorkingDirectory=/home/${USER}/ci_cd
            # WorkingDirectory=~/3.2-crud_for_server_postgre
            # Старт проекта:
            # Путь к исполняемому файлу - /home/pashtet/3.2-crud_for_server_postgre/activate/bin/gunicorn
            # Максимальное количество экземпляров проекта (создается для обработки повышенной нагрузки, зависит от кол-ва ядер процессора, как правила по два процесса на ядро) - stocks_products.wsgi:application --wo>
            # Создание сокета через который вебсервер будет подключаться к gunicorn - unix:/home/${USER}/3.2-crud_for_server_postgre/stocks_products/project.sock
            ExecStart=/home/${USER}/ci_cd/env/bin/gunicorn stocks_products.wsgi:application --workers=3 -b unix:/home/${USER}/ci_cd/stocks_products/project.sock

            [Install]
            WantedBy=multi-user.target"

        echo "$CONFIG_gunicorn_service" | sudo tee /etc/systemd/system/gunicorn.service && echo [ create gunicorn_service ]
    else
        clear
        echo "****************************************"
        echo "----------------------------------------"
        echo "Вы не должны быть root, файлы не созданы"
        echo "----------------------------------------"
        echo "****************************************"
fi
