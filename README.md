# python_pw

Проект для автоматизированного тестирования web-приложений на Python + Playwright + pytest.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chrome  # либо: playwright install (поставит все движки)
brew install allure        # CLI для генерации/просмотра HTML-отчёта (macOS)
```

## Конфигурация

Настройки задаются через `.env` (см. `.env.example`):

```bash
cp .env.example .env
```

| Переменная        | Описание                                              | По умолчанию |
|--------------------|--------------------------------------------------------|--------------|
| `BASE_URL`          | Базовый URL тестируемого приложения                    | пусто        |
| `BROWSER_ENGINE`    | Движок Playwright: `chromium` \| `firefox` \| `webkit` | `chromium`   |
| `BROWSER_CHANNEL`   | Канал chromium: `chrome` \| `msedge` \| пусто          | `chrome`     |
| `HEADLESS`          | Запуск без UI (`true`/`false`)                          | `true`       |
| `SLOW_MO`           | Задержка между действиями Playwright, мс                | `0`          |
| `VIEWPORT_WIDTH`    | Ширина окна браузера                                    | `1920`       |
| `VIEWPORT_HEIGHT`   | Высота окна браузера                                    | `1080`       |
| `DEFAULT_TIMEOUT`   | Таймаут ожидания элементов/действий, мс                 | `15000`      |
| `LOGIN` / `PASSWORD`| Учётные данные для авторизации                          | —            |
| `PRODUCTS`          | Товары для тестов корзины/заказа, через запятую (1 и более) | `Sauce Labs Backpack,Sauce Labs Bike Light` |

По умолчанию тесты запускаются в реальном Chrome (`BROWSER_ENGINE=chromium` + `BROWSER_CHANNEL=chrome`).
Чтобы переключиться на Firefox или WebKit, поменяйте `BROWSER_ENGINE` в `.env`, либо передайте флаг явно:

```bash
pytest --browser firefox
```

## Запуск тестов

```bash
pytest                          # все тесты, headless-режим согласно .env
pytest -v                       # подробный вывод
HEADLESS=false pytest           # запуск с видимым браузером
pytest tests/ui/test_login.py   # запуск конкретного теста
```

## Отчёты Allure

Результаты прогона автоматически пишутся в `allure-results/` (см. `addopts` в `pytest.ini`),
директория очищается перед каждым запуском в `conftest.py` — не флагом `--clean-alluredir`,
т.к. под `pytest-xdist` каждый воркер вызывает `pytest_configure` самостоятельно, а очистка
внутри allure-pytest ничем не защищена (`shutil.rmtree` без блокировки): один воркер может
снести результаты, уже записанные другим. Поэтому чистим один раз в главном процессе, до
того как xdist порождает воркеров (проверка `not hasattr(config, "workerinput")`). Дальше
нужно сгенерировать и открыть HTML-отчёт:

```bash
pytest                                          # прогон, результаты в allure-results/
allure generate allure-results --clean -o allure-report
allure open allure-report                       # откроет отчёт в браузере
```

Либо одной командой (сгенерирует, поднимет локальный сервер и откроет отчёт):

```bash
allure serve allure-results
```

В отчёте у каждого теста расписаны шаги (`@allure.step` в Page Object'ах), а к упавшим
тестам автоматически прикладывается скриншот страницы на момент падения (см. `conftest.py`).

## Параллельный запуск

Тесты независимы друг от друга (каждый сам логинится и создаёт своё состояние), поэтому их
можно гонять параллельно через `pytest-xdist`:

```bash
pytest -n auto     # по одному воркеру на ядро CPU
pytest -n 4         # фиксированное число воркеров
```

## CI (GitHub Actions)

Workflow [.github/workflows/ci.yml](.github/workflows/ci.yml) гоняет весь набор тестов в
headless-режиме на `ubuntu-latest` при каждом push/PR в `main`: ставит зависимости, браузер
Chrome, запускает `pytest -n auto` и прикладывает `allure-results` как артефакт прогона
(доступен на вкладке Actions → конкретный ран → Artifacts).

## Структура проекта

```
.github/workflows/  # CI-пайплайн (GitHub Actions)
config/              # настройки проекта (config/settings.py читает .env)
pages/               # Page Object'ы (base_page.py — базовый класс, шаги авторизации/каталога/корзины/чекаута)
tests/ui/            # UI-тесты (логин, добавление в корзину, оформление заказа)
conftest.py          # фикстуры pytest-playwright + allure (настройки браузера, скриншот на падении)
```
