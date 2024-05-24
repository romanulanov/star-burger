#!/bin/bash

set -e

APP_PATH="/opt/star-burger"

# Переходим в директорию приложения
cd $APP_PATH

echo " Обновляем код из репозитория"
git pull
echo "Код репозитория обновлён"

echo "Устанавливаю npm зависимости..."
npm ci --dev
echo "NPM зависимости успешно установлены."

echo "Собираю фронтенд..."
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
echo "Фронтенд успешно собран."

python3 -m venv venv
echo "Создал окружение"
echo "Активирую виртуальное окружение Python..."
source venv/bin/activate

echo "Устанавливаю зависимости Python..."
pip3 install -r requirements.txt

echo "Python зависимости успешно установлены."

echo "Пересобираю статические файлы Django..."
python3 manage.py collectstatic
echo "Пересобрал статику Django"

echo "Применяю миграции Django..."
python3 manage.py migrate --noinput
echo "Накатил миграции"

echo "Перезапускаю службу starburger"
systemctl restart starburger.service
echo "Перезагружаю Nginx..."
systemctl reload nginx
echo "Перезапустил сервисы Systemd"

deactivate
echo "Деактивировал окружение"

echo "Деплой успешно завершён!"