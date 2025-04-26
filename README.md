# Домашняя работа к модулю 9

# Тема 34.2 Docker Compose

## 1. Сервис для работы PostgreSQL
1. Создаём сеть dbnet (driver: bridge) для организации взаимодействия внутри контейнера.
    docker network dbnet
2. Скачивает из Docker Hub официальный образ Postgres 17-alpine.
3. Создаём контейнер:
    docker run -d --rm \
    --network dbnet \
    --name psgr \
    -e POSTGRES_DB=mydb \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=1234 \
    -v postgres-data:/var/lib/postgresql/data \
    postgres:17-alpine

## 2. Сервис для работы Adminer
1. Скачаем образ приложение для администрирования БД - adminer.
2. Создаём контейнер:
    docker run -d --rm \
    --network dbnet \
    --name psgr_adminer \
    --link psgr:db \
    -p 8080:8080 \
    adminer
3. Перейдём по адресу "localhost:8080" в браузере попадём на страницу adminer.

## 3. Создадим compose.yaml
