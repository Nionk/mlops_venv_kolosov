# Отчёт: окружения и зависимости Python

## 1. Информация о системе и инструментах
- Операционная система: Windows NT (win32)
- Версия Python: Python 3.12.7
- Версия Poetry: Poetry (version 2.5.1)

```powershell
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\pip_project> python --version
Python 3.12.7

PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> poetry --version
Poetry (version 2.5.1)
```

## 2. Пути к интерпретаторам обеих частей
- Часть 1 (`pip_project`):
```powershell
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\pip_project> python -c "import sys; print(sys.executable)"
C:\Users\Admin\MyWork\ml_ops\practice_2_result\pip_project\.venv\Scripts\python.exe
```
- Часть 2 (`poetry_project`):
```powershell
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> poetry env info --executable
C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project\.venv\Scripts\python.exe
```

## 3. Список прямых зависимостей и их назначение
- `requests` — выполнение HTTP-запросов к API Open-Meteo.
- `pandas` — табличная обработка данных и работа с временными рядами.
- `matplotlib` — визуализация данных и сохранение графиков.
- `pytest` (группа `test`) — запуск модульных тестов.
- `ruff` (группа `dev`) — линтер и форматтер кода.

## 4. Транзитивные зависимости
По выводу `poetry show --tree`:
- `requests` -> `urllib3`
- `pandas` -> `numpy`
- `matplotlib` -> `pillow`

## 5. Результат восстановления окружения `pip_project`
После удаления директории `.venv` и выполнения повторной установки из файла зависимостей окружение успешно восстановилось.

```powershell
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\pip_project> python -m pip install -r requirements.txt
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\pip_project> python plt_temp.py
Сохранено в temperature_24h.csv
```

## 6. Результат проверки групп Poetry

```powershell
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> $env:PYTHONPATH="."; poetry sync --only main
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> $env:PYTHONPATH="."; poetry sync --only test
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> $env:PYTHONPATH="."; poetry sync
```

- `poetry sync --only main`: выбранные группы (`main`), `pytest` и `ruff` недоступны, `plt_temp.py` запускается.
- `poetry sync --only test`: выбранные группы (`test`), `pytest` падает при импорте `pandas`, `ruff` недоступен, `plt_temp.py` выдает ошибку `ModuleNotFoundError`.
- `poetry sync`: выбранные группы (`main`, `test`, `dev`), все инструменты и скрипты работают.

## 7. Объяснение изменений после точечного обновления зависимости
При изменении диапазона прямой зависимости в `pyproject.toml` и вызове обновления:

```powershell
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> poetry update requests
Updating dependencies
Resolving dependencies... (0.2s)
No dependencies to install or update
```

- Изменение ограничения в `pyproject.toml`: `"requests (>=2.34.2,<3.0.0)"` -> `"requests (>=2.31.0,<3.0.0)"`.
- Изменение в `poetry.lock`: Обновился только `content-hash`, так как версия `2.34.2` уже являлась самой свежей в рамках заданного диапазона. Обновление не выходит за границы диапазона во избежание несовместимости мажорных версий.

## 8. Результат чистого восстановления Poetry-проекта
После удаления папки `.venv` и повторного развертывания проекта:

```powershell
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> Remove-Item -Recurse -Force .venv
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> poetry install
Installing dependencies from lock file
...
PS C:\Users\Admin\MyWork\ml_ops\practice_2_result\poetry_project> $env:PYTHONPATH="."; poetry run pytest
tests\test_dataframe.py .                                                          [100%]
================================== 1 passed in 11.69s ===================================
```

## 9. Краткое сравнение подходов `venv + pip` и Poetry
- `venv + pip`: Изоляция достигается стандартным модулем `venv`, а воспроизводимость обеспечивается плоским файлом `requirements.txt` (полученным через `pip freeze`), содержащим все прямые и транзитивные зависимости вперемешку без разделения по назначению.
- Poetry: Разделяет намерения разработчика (`pyproject.toml` с диапазонами версий и группами) и жесткую фиксацию состояния окружения (`poetry.lock` с контрольными суммами и точными версиями), что дает реальную идентичность развертывания на любых машинах.