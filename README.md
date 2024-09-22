### Задание 1

Перейдите в директорию **task_1**:
```bash
cd task_1  
```
  
Далее необходимо собрать контейнеры:
```bash
docker compose up --build -d
```  
  
После того, как контейнеры собраны swagger будет доступен в строке браузера:
```
http://localhost:8000/docs  
```
  
В рамках задачи реализованы 3 эндпойнта, выполняющих действия описанные в техническом задании.  
### Задание 2  
  
Перейдите в директорию **task_2**  
```
cd task_2  
```
  
Далее поднимаем базу данных:  
```bash
docker-compose up -d  
```

При старте БД исполняется скрипт init.sql, который создает таблицы **full_names** и **short_names**, после чего заполняет их  данными 

Далее заходим в контейнер:    
```bash
docker exec -it 'db' '/bin/bash'  
```
  
Запускаем psql:
```bash
psql -U postgres  
```
  
Первый вариант SQL запроса для решения этой задачи:
```sql
UPDATE full_names AS fn
SET status = sn.status
FROM short_names AS sn
WHERE sn.name = split_part(fn.name, '.', 1);
```

Второй вариант SQL запроса для решения этой задачи, похож на первый, но с использованием CTE:
```sql
WITH matched_names AS (
    SELECT
        fn.name AS full_name,
        sn.status AS status
    FROM
        full_names AS fn
    JOIN
        short_names AS sn
    ON
        sn.name = split_part(fn.name, '.', 1)
)
UPDATE full_names AS fn
SET status = mn.status
FROM matched_names AS mn
WHERE fn.name = mn.full_name;
```
Для того чтобы очистить данные достаточно сделать:  
```bash
docker-compose down  
```

Это удалит таблицы из контейнера, и при следующем **docker compose up** БД будет создана  с первоначальным состоянием.
