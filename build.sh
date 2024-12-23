#!/bin/bash

# Выходим из скрипта, если какая-либо команда завершится с ошибкой
set -e

# Проверяем, что docker-compose установлен
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose не установлен. Пожалуйста, установите его перед запуском скрипта."
    exit 1
fi

# Собираем и запускаем проект с помощью docker-compose
echo "Запускаем Docker Compose..."
docker-compose up -d --build

echo "Проект запущен. Вы можете открыть браузер и перейти по адресу http://localhost:5000"
