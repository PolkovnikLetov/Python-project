#!/bin/bash

# Установите имя образа
IMAGE_NAME=python-project

# Соберите Docker-образ
docker build -t $IMAGE_NAME .

# Запустите контейнер
docker run -p 5000:5000 $IMAGE_NAME
