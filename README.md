# neighbors - тестовое задание

### требования
* python 3.x
* pip 

### устновка
``` bash
# git clone https://github.com/hanurp/neighbors.git
# cd neighbors
# cp neighbors/settings.default.py neighbors/settings.py
# pip install -r requirements.txt
```
### тестирование
``` bash
python manage.py test
```

### использование
запуск dev сервера
``` bash
python manage.py runserver
```
#### список пользователей
http://localhost:8000/persons/

#### добавить пользователя
нужно отправить POST запрос на адрес:

http://localhost:8000/persons/

в теле JSON
``` json
{
    "name": "Max",
    "lon": 37.545608,
    "lat": 55.881626
}    
```
#### Вывод ближайших N людей по координатам
http://localhost:8000/persons/nearby/?lon=37.545608&lat=55.881626&limit=99
