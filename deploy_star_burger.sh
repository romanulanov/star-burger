#!/bin/bash

set -e

<<<<<<< Updated upstream
source .env
=======
source .env 
>>>>>>> Stashed changes

APP_PATH="/opt/star-burger"

# Переходим в директорию приложения
cd $APP_PATH

echo " Обновляем код из репозитория"
git pull
echo "Код репозитория обновлён"

echo "Устанавливаю npm зависимости..."
npm ci --dev
echo "NPM зависимости успешно установлены."

<<<<<<< Updated upstream
python3 -m venv venv
=======
python3 -m venv venv 
>>>>>>> Stashed changes
echo "Создал окружение"

echo "Активирую виртуальное окружение Python..."
source venv/bin/activate

echo "Устанавливаю зависимости Python..."
pip3 install -r requirements.txt

echo "Python зависимости успешно установлены."

echo "Пересобираю статические файлы Django..."
python3 manage.py collectstatic --noinput
echo "Пересобрал статику Django"

echo "Применяю миграции Django..."
python3 manage.py migrate --noinput
echo "Накатил миграции"

echo "Перезапускаю службу starburger"
systemctl restart starburger.service
echo "Перезагружаю Nginx..."
systemctl reload nginx
echo "Перезапустил сервисы Systemd"

commit=$(git rev-parse HEAD)

curl -H "X-Rollbar-Access-Token: $ROLLBAR_TOKEN" \
<<<<<<< Updated upstream
             -H "accept: application/json" \
                  -H "content-type: application/json" \
                       -X POST "https://api.rollbar.com/api/1/deploy" \
                                                   -d '{
=======
	     -H "accept: application/json" \
	          -H "content-type: application/json" \
		       -X POST "https://api.rollbar.com/api/1/deploy" \
		            -d '{
>>>>>>> Stashed changes
  "environment": "production",
    "revision": "'"$commit"'",
      "rollbar_username": "'$(whoami)'",
        "local_username": "'$(whoami)'",
<<<<<<< Updated upstream
          "comment": "deploy",
            "status": "succeeded"
=======
	  "comment": "deploy",
	    "status": "succeeded"
>>>>>>> Stashed changes
    }'
echo "Отправил информацию в роллбар"
deactivate
echo "Деактивировал окружение"

<<<<<<< Updated upstream
echo "Деплой успешно завершён!"
=======
echo "Деплой успешно завершён!"
>>>>>>> Stashed changes
