Здесь собраны результаты практических работ по курсу Проетирование баз данных (ИС26).
## Полные задания лабораторных
1. [Lab1](https://github.com/Almaxana/DataBaseWork/blob/main/Labs/Lab1.pdf)
2. [Lab2](https://github.com/Almaxana/DataBaseWork/blob/main/Labs/Lab2.pdf)
3. [Lab3](https://github.com/Almaxana/DataBaseWork/blob/main/Labs/Lab3.pdf)
4. [Lab4](https://github.com/Almaxana/DataBaseWork/blob/main/Labs/Lab4.pdf)
5. [Вопросы к экзамену](https://github.com/Almaxana/DataBaseWork/blob/main/Labs/ExamQuestions.pdf)

## Содержание работ
### 1. Подготовка и проектирование
БД содержит данные о работе **магазина музыкальных инструментов**. Более подробную информацию пожно увидеть на ER диаграмме
![ERD](https://github.com/Almaxana/DataBaseWork/blob/main/imgs/ERD.png)

БД находится в 3 НФ


### 2.Развертывание СУБД внутри docker-контейнера, создание таблиц и заполнение данными.
#### 2.1 Развертывание и Создание отношений
БД развернута в контенере ```db```, который описан в сервисе ```db``` в  [docker-compose.yml](https://github.com/Almaxana/DataBaseWork/blob/main/docker-compose.yml).    

При создании нового контейнера автоматически запускается скрипт [creation.sh](https://github.com/Almaxana/DataBaseWork/blob/main/migrations/creation.sh), который в свою очередь запускает идемпотентные файлы [миграции](https://github.com/Almaxana/DataBaseWork/tree/main/migrations/numbered_migrations) по созданию отношений (1.01 - 1.11), пользователей и ролей (1.12 - 1.16). Через [env](https://github.com/Almaxana/DataBaseWork/blob/main/.env) есть возможность передать версию, до которой будут происходить миграции.

Роли:
 - reader (может только читать данные из таблиц, но не изменять их)
 - writer (может читать и добавлять, изменять данные, но не может их удалять)
 - group_role
 
Пользователи:
 - analytic (имеет доступ на чтение толкьо таблицы users)
 - n пользователей (могут быть подключены к БД и присоединены к group_role)
 

#### 2.2 Заполннеие таблиц данными
После создания таблицы заполняются тестовыми данными. Для этого есть отдельный контейнер ```pyInsert``` (side car). При его старте запускается [start_insert_migrations.py](https://github.com/Almaxana/DataBaseWork/blob/main/py/start_insert_migrations.py), который в свою очередь для каждой таблицы запускает один из [скриптов](https://github.com/Almaxana/DataBaseWork/tree/main/py/py_migrations), генерирующий данные для добавления в БД. Кол-во записей для генерации можно передать через [env](https://github.com/Almaxana/DataBaseWork/blob/main/.env).



## Администрирование и оптимизация
### Оптимизация
1. Написан [скрипт](https://github.com/Almaxana/DataBaseWork/blob/main/py/explain/ExplainQueries.py), запускающий ```ExplainAnalyze``` для нескольких запросов для измерения времени их выполнения.

2. Затем отношения индексируются и запускается подобный скрипт, для анализа изменения скорости выполнения этих же запросов.
3. Далее через [скрипт](https://github.com/Almaxana/DataBaseWork/blob/main/py/explain/partititonCreation.py) создаются партиции, и так же запускается скрипт для анализа скорости выполнения запросов.

Сводная даблица времени запуска
![https://github.com/Almaxana/DataBaseWork/blob/main/QueriesAnalisis.png](https://github.com/Almaxana/DataBaseWork/blob/main/imgs/QueriesAnalisis.png)

### Backups

Написан [скрипт](https://github.com/Almaxana/DataBaseWork/blob/main/py/backups/backupCreation.py), создающий бэкап БД каждые n часов. Последние m бэкапов хранятся, более старые удаляются. Параметры n и m можно передать через [env](https://github.com/Almaxana/DataBaseWork/blob/main/.env).

### Реплицирование через Patroni

Развернуто 2 реплики (всего 3 ноды) с использованием [Patroni](https://github.com/patroni/patroni). При отказе мастера происходит автоматическое переключение.

## Мониторинг

В отдельных контейнерах развернуты Prometheus и Grafana
![Grafana example](https://github.com/Almaxana/DataBaseWork/blob/main/imgs/Grafana_ex.jpg)
