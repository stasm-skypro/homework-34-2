# Домашняя работа к модулю 9

# Тема 34.2 Docker Compose

## 1. Структура и описание сервисов

Весь проект разбит на 5 сервисов (контейнеров):

### -- postgres - сервис базы данных PostgreSQL.

Контейнер с БД. Используется готовый образ postgres:17-alpine.

### -- adminer - сервис интерфейса администрирования базы данных.

Используется готовый образ adminer.

После запуска сервиса, Adminer доступен по адресу: http://localhost:8080

![adminer](./media/readme_pic/adminer.png)

Параметры входа в Adminer:

-- server: psgr

-- db_user: school_admin

-- db_password: 1234

-- db_name: school

### -- redis - сервис базы данных Redis.

Используется готовый образ redis:latest.

### -- web - сервис веб-сервера (django).

Образ создаётся с помощью Dockerfile. Фикстуры для заполнения БД находятся внутри проекта в директориях "materials/fixtures" и "users/fixtures".

Применение фикстур:

```bash
docker-compose exec web python manage.py loaddata \ 
/materials/fixtures/course_fixture.json \ 
/materials/fixtures/lesson_fixture.json \ 
/users/fixtures/payment_fixture.json \ 
/users/fixtures/subscription_fixture.json \ 
/users/fixtures/user_fixture.json
```

### -- celery - сервис Celery, используется для запуска периодических задач.

Образ создаётся с помощью Dockerfile.


## 2. Запуск Docker Compose локально

```bash
docker compose up --build
```

Результат работы:

![containers](./media/readme_pic/containers.png)


## 3. Описание решений

Celery выделен в отдельный контейнер. Для работы контейнера с Celery нужно создать тот же самый образ, что и для web-контейнера. Это очень хорошо видно по их размеру. Неоднозначное решение. Но так сделано. При запуске контейнера celery возникла проблема - для запуска нужно применить миграции и запустить celery-beat. Но если сделдать это командой:

```bash -c "python manage.py migrate && celery -A config worker --loglevel=info"``` в секции command,

то возникает ошибка: миграции не успевают примениться и происходит запуск celery-beat. Чтобы исправить эту проблему, пришлось создать дополнительный исполняемый файл entrypoint_selery.sh, который проверяет готовность базы данных, применяет миграции и запускает celery-beat. Для работы entrypoint_selery.sh в Dockerfile добавлена установка netcat и 
entrypoint_selery.sh делается исполняемым. 

Точно таким же способом и с той же целью сохдан исполняемый файл entrypoint_web.sh, который проверяет готовность базы данных, применяет миграции и запускает веб-сервер в контейнере web.


## 4. Известные проблемы

При запуске swaggera происходит ошибка в ручке пользователя, конкретно в методе get_serializer_class. Причина известна: 
Когда DRF строит схемы для Swagger/Redoc, он вызывает get_serializer_class() не во время реального запроса, а на этапе подготовки документации. Именно в этот момент у self.request и self.get_object() ещё нет реальных данных. А в коде у меня написано:

```python
def get_serializer_class(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            if self.request.user == self.get_object():
                ...
```
Я так понимаю, что нужно переписать get_serializer_class() без вызова self.get_object(). А отличать "свой профиль" от "чужого" в сериализатое. Но для этого нужно сделать много рефакторинга и пока не понимаю как.
