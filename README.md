# Alial Server Management CLI

CLI для подключения к серверам АЛИАЛ ГРУПП.

## Установка

2. Клонируйте проект на ваш компьютер и перейдите в него:

```bash
git clone http://git.alial.group/a.pankrashov/asmcli.git
cd asmcli
```

3. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Установите зависимости:

```bash
pip install requirements.txt
```

4. Скопируйте `entries.json.example` как `entries.json` и заполните файл.

3. Добавьте проект в `PATH` ([инструкция](https://remontka.pro/add-to-path-variable-windows/)).

## Настройка

Внесите доступы ко всем серверам хранятся в файле `entries.json` по следующей схеме

```json
[
  {
    "name": "myserver", # имя одного entry
    "cwd": "X:\\path\\to\\cwd", # рабочая директория с файлами подключений
    "target": "connect.bat", # основной файл подключения
    "subtargets": [
      ".\\someprocess.exe" # список дополнительных файлов (чтобы открывать txt-файлы, директории и окна браузера)
    ],
    "c2c": "copymetocliboard" # данный текст копируется в буфер обмена, чтобы не искать и не копировать пароль
  }
]
```

## Использование

Запуск в командной строке

```bash
asmcli --entry_name=myserver
```

## Contributing

Приветствуются запросы на слияние (`pull requests`). Для внесения серьёзных изменений описывайте проблему в обсуждении (`issue`) для согласования доработок.

## Лицензия

[MIT](http://git.alial.group/a.pankrashov/asmcli/raw/branch/master/LICENSE)