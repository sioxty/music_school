# Музична школа — CLI програма

Проста CLI-система обліку музичної школи на Python + SQLAlchemy + Click.

## Особливості

- CRUD для учнів, викладачів, предметів, груп, занять та оцінок
- Доменна модель з SQLAlchemy 2.0
- Патерн Repository для роботи з базою
- CLI розділений на окремі модулі у `cli/`
- Можливість наповнення демонстраційними даними
- Тести для CLI та фікстур

## Встановлення

### Через `pip`

```bash
git clone https://github.com/sioxty/music_school.git
cd cursova
pip install -r requirements.txt
```

### Через `uv`

```bash
git clone https://github.com/sioxty/music_school.git
cd cursova
uv sync --active
```

> Після цього можна запускати CLI команду через `uv run main.py --help`.

## Запуск програми

```bash
python3 main.py --help
```
або через uv
```bash
uv run main.py --help
```

### Доступні групи команд

- `student` — учні
- `teacher` — викладачі
- `subject` — предмети
- `group` — групи
- `lesson` — заняття
- `grade` — оцінки
- `report` — звіти
- `seed` — наповнення бази даними

## Наповнення демонстраційними даними

```bash
python3 main.py seed demo
```
або через uv
```bash
uv run main.py seed demo
```

## Приклади використання

```bash
python3 main.py student list
python3 main.py teacher add
python3 main.py lesson add
python3 main.py lesson list --group-id 1
python3 main.py grade list-lesson 1
python3 main.py group show 1
```

## Тести

```bash
uv run python -m unittest discover -s tests -p 'test_*.py'
```

## Структура проекту

- `main.py` — точка входу CLI
- `database.py` — налаштування SQLAlchemy, сесії і наповнення даними
- `models.py` — ORM-моделі домену
- `repository.py` — generic репозиторій + конкретні репозиторії
- `cli/` — CLI-групи команд
- `reports.py` — функції звітності
- `tests/` — тести та фікстури

## Примітки

- База зберігається у файлі `school.db`
- Усі оголошені команди можна переглянути через `--help`
- Друкування звʼязаних обʼєктів відбувається всередині сесії, щоб уникнути `DetachedInstanceError`
