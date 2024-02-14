# unittest_practice - Untit-тесты для новостного приложения

## Стек:

- Python 3.9;
- Django 3.2.16;
- Python Unittest & Pytest.

## Запуск проекта:

#### Развернуть виртуальное окружение:
- Linux/MacOS:
```Bash
python3 -m venv venv
```

- Windows:
```Bash
python -m venv venv
```

#### Активировать виртуальное окружение:
```Bash
source venv/bin/activate
```

#### Установить зависимости:
- Обновить pip:
```Bash
python -m pip install --upgrade pip 
```

- Установить зависимости:
```Bash
pip install -r requirements.txt
```

#### Применить миграций:
- Linux/MacOS:
```Bash
python3 manage.py migrate
```

Для загрузки заготовленных новостей после применения миграций выполните команду:

```Bash
python manage.py loaddata news.json
```
---
Автор: [Сергей Кульбида](https://github.com/SergeyKDEV)
