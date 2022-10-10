# yamdb_final
![yamdb_workflow](https://github.com/sharumrio/yamdb_final/workflows/yamdb_workflow/badge.svg)
### YaMDb о проекте и авторах:
Проект является агрегатором отзывов о фильмах, книгах и музыке

Список разработчиков:
- [Гусейнов Нажмудин](https://github.com/Casp1an "https://github.com/Casp1an.com")
- [Халус Кузьма](https://github.com/Domovoy-k "https://github.com/Domovoy-k")
- [Шайхнисламов Марат](https://github.com/Sharumario "https://github.com/Sharumario")

### Пример заполнения env:

DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql

DB_NAME=postgres - имя базы данных

POSTGRES_USER=postgres - логин для подключения к базе данных

POSTGRES_PASSWORD=postgres - пароль для подключения к БД (установите свой)

DB_HOST=db - название сервиса (контейнера)

DB_PORT=5432 - порт для подключения к БД

### Запуск контейнера:

cd infra/ - переходим в директорию

docker-compose up -d --build - запускаем контейнер

docker-compose exec web python manage.py migrate - делаем миграции

docker-compose exec web python manage.py createsuperuser - создаём супер пользователя

### Заполнение базы данных:
Можно осуществить загрузку тестовых данных из приложенных .csv файлов командой:

docker-compose exec web python manage.py upload_csv_files

Затем нужно зайти на http://localhost/admin/, авторизоваться и начинать вносить свой записи в бд.

Резервную копию базы данных можно создать командой:

docker-compose exec web python manage.py dumpdata > fixtures.json 

### Полное описание проекта с примерами запросов:

http://localhost/redoc/
