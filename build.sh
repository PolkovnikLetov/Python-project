#!/bin/bash


set -e


if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose не установлен. Пожалуйста, установите его перед запуском скрипта."
    exit 1
fi


echo "Запускаем Docker Compose..."
docker-compose up -d --build

echo "http://localhost:5000"