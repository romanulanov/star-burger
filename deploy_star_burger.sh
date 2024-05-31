#!/bin/bash

set -e

source .env

APP_PATH="/opt/star-burger"

# Переходим в директорию приложения
cd $APP_PATH

echo " Обновляем код из репозитория"
git pull
echo "Код репозитория обновлён"

echo "Устанавливаю npm зависимости..."
npm ci --dev
echo "NPM зависимости успешно установлены."

echo "Отключаем фоновую сборку фронтенда"

parcel_processes=$(ps aux | grep 'parcel' | grep -v 'grep' | awk '{print $2}')
if [ -n "$parcel_processes" ]; then
          echo "Завершаем процессы Parcel: $parcel_processes"
            kill -9 $parcel_processes
    else
              echo "Процессы Parcel не найдены"
fi

echo "Собираем фронтенд"
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

python3 -m venv venv
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
             -H "accept: application/json" \
                  -H "content-type: application/json" \
                       -X POST "https://api.rollbar.com/api/1/deploy" \
                                                   -d '{
  "environment": "production",
    "revision": "'"$commit"'",
      "rollbar_username": "'$(whoami)'",
        "local_username": "'$(whoami)'",
          "comment": "deploy",
            "status": "succeeded"
    }'
echo "Отправил информацию в роллбар"
deactivate
echo "Деактивировал окружение"

echo "Деплой успешно завершён!"