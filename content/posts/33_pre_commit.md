---
title: "Использование pre-commit"
date: 2023-01-23T11:17:40+03:00
categories: ["git"]
---

Если кто-то ещё не использует, советую попробовать внедрить такой инструмент как [pre-commit](https://pre-commit.com/#install).

<!--more-->

## Зачем?
Позволяет автоматически запускать проверки кода, линтеры, авто тесты локально перед коммитом.

Плюсы:
- Дешевле во всех смыслах (Чем полноценный CI)
- Устраняем человеческий фактор, да можно отключить, но в целом проверка автоматизировна
- Код становится чище и легче в поддержке
- Дополнительные Quality Gate на стороне разработчика
- Дополнительная уверенность что всё ок (при хорошем покрытии тестами)

Минусов за время использования не заметил, только если то, что требуется время на внедрение в проект и в команду для наибольшей выгоды.
Например, на одном из хакатонов, мы его отключали чтобы не тормозить разработку, но там другие критерии и основной - скорость.

## Установка

Установка достаточно простая (можно в виртуальном окружении):
```bash
pip install pre-commit  
```

Установка git hook из корня репозитория  
```bash
pre-commit install  
```

И конфигурационный файл: `.pre-commit-config.yaml`

Пример:
```yaml
repos:  
-   repo: https://github.com/pre-commit/pre-commit-hooks  
    rev: v3.2.0  
    hooks:  
    -   id: trailing-whitespace  
    -   id: end-of-file-fixer  
    -   id: check-yaml  
    -   id: check-xml  
    -   id: check-ast  
    -   id: check-json  
    -   id: check-added-large-files  
  
-   repo: https://github.com/PyCQA/flake8  
    rev: 4.0.1  
    hooks:  
    -   id: flake8  
        args: [--max-line-length=120]
```

Всё, после этого после commit-а будут прогоняться указанные вами проверки только на тех файлах которые вы меняли.

Список доступных hooks можно посмотреть [здесь](https://pre-commit.com/hooks.html)

Оптионально, можно сразу прогнать на всех файлах:
```
pre-commit run --all-files
```

НО, если проект большой, то это приведёт к большому числу изменений. Надо смотреть по ситуации.

## Рецепты

### Python
Пример, с запуском python юнит тестов через pytest (запускаются все тесты, даже если не меняли их) можно найти [здесь](https://github.com/arybin93/hw-template/blob/master/.pre-commit-config.yaml)

Так же используется:
- black (автоматически форматирует код)
- isort (расставляет импорты в порядке) 

Но тоже надо смотреть по ситуации, иногда творится уже совсем настоящая магия и лучше её избегать, может быть непредсказуемый результат в итоге. 

На последних проектах, я их не использую.

### Python unit tests in Docker

Для запуска тестов в docker image:
- поменять как минимум `<working_dir>` и `<docker_image>` в entry.
- Настроить запуск тестов под себя

Пример:
```yaml
repos:
  - repo: local # Use a local repository
    hooks:
      - id: docker-pytest
        name: pytest
        language: docker_image
        entry: --entrypoint "/bin/bash" -v "pwd":/<working_dir> --user root <docker_image> -c "pytest -v tests/"
        pass_filenames: false
        always_run: true
        verbose: true
```
