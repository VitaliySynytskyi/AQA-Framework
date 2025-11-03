# Quick Start Guide - AQA Framework

## ⚡ Швидкий старт за 5 хвилин

### Крок 1: Клонування та налаштування (2 хв)

```powershell
# Клонуємо репозиторій
git clone https://github.com/VitaliySynytskyi/AQA-Framework.git
cd "AQA Framework"

# Створюємо віртуальне середовище
python -m venv venv

# Активуємо (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Встановлюємо залежності
pip install -r requirements.txt
```

### Крок 2: Перший запуск (1 хв)

```powershell
# Запускаємо unit тести
pytest unit_tests/ -v

# Запускаємо один BDD тест
behave features/search.feature
```

### Крок 3: Перегляд результатів (2 хв)

```powershell
# Дивимося покриття коду
pytest unit_tests/ --cov=. --cov-report=html
start htmlcov/index.html

# Запускаємо з Allure звітами
behave features/ --format allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

## 📋 Основні команди

### BDD тести
```powershell
# Всі тести
behave features/

# Конкретна feature
behave features/search.feature

# Headless режим
$env:HEADLESS="true"; behave features/
```

### Unit тести
```powershell
# Всі тести з покриттям
pytest unit_tests/ -v --cov=. --cov-report=term

# Конкретний файл
pytest unit_tests/test_home_page.py -v

# З HTML звітом
pytest unit_tests/ --html=report.html
```

## 🎯 Що протестувати спочатку?

### 1. Пошук товарів
```bash
behave features/search.feature
```
- ✅ 8 сценаріїв пошуку
- ⏱️ ~2-3 хвилини

### 2. Кошик покупок
```bash
behave features/cart.feature
```
- ✅ 8 сценаріїв кошика
- ⏱️ ~3-4 хвилини

### 3. Сортування
```bash
behave features/sorting.feature
```
- ✅ 5 сценаріїв сортування
- ⏱️ ~2 хвилини

## 🔧 Налаштування

### Зміна браузера
```powershell
# Chrome (default)
behave features/

# Firefox
$env:BROWSER="firefox"; behave features/

# Edge
$env:BROWSER="edge"; behave features/
```

### Headless режим
```powershell
$env:HEADLESS="true"
behave features/
```

### Зміна таймаутів
Відредагуйте `config/config.yaml`:
```yaml
timeouts:
  short: 5
  medium: 10
  long: 30
```

## 📊 Структура проекту (спрощено)

```
├── features/              # BDD тести (Gherkin)
│   ├── *.feature         # Тестові сценарії
│   ├── steps/            # Реалізація кроків
│   └── environment.py    # Налаштування Behave
├── pages/                # Page Objects
│   ├── home_page.py     # Головна сторінка
│   ├── search_page.py   # Пошук
│   └── cart_page.py     # Кошик
├── framework/            # Ядро фреймворку
│   ├── browser_manager.py
│   └── config_manager.py
├── unit_tests/           # Unit тести
└── config/               # Конфігурація
    └── config.yaml
```

## 🐛 Troubleshooting

### Проблема: "Import could not be resolved"
**Рішення**: Встановіть залежності
```powershell
pip install -r requirements.txt
```

### Проблема: "WebDriver not found"
**Рішення**: webdriver-manager встановить автоматично при першому запуску

### Проблема: Тести падають на українському сайті
**Рішення**: Локатори налаштовані для rozetka.com.ua

### Проблема: Повільне виконання
**Рішення**: Використайте headless режим
```powershell
$env:HEADLESS="true"
behave features/
```

## 📖 Детальна документація

- `README.md` - Повний опис проекту
- `ARCHITECTURE.md` - Архітектура фреймворку
- `RUNNING_TESTS.md` - Детальна інструкція по запуску

## 🎓 Навчальні приклади

### Приклад 1: Простий BDD тест
```gherkin
Scenario: Search for laptop
  Given I am on the Rozetka home page
  When I search for "ноутбук"
  Then I should see search results
```

### Приклад 2: Unit тест
```python
def test_search_product(self, home_page):
    home_page.search_product("laptop")
    assert home_page.driver.get.called
```

### Приклад 3: Використання Page Object
```python
from pages.home_page import HomePage

page = HomePage(driver)
page.open_home_page()
page.search_product("iPhone")
```

## 💡 Поради

1. **Завжди запускайте unit тести перед BDD**
   ```powershell
   pytest unit_tests/ -v && behave features/
   ```

2. **Використовуйте конкретні features для швидкої перевірки**
   ```powershell
   behave features/search.feature::8  # Запустить 8-й сценарій
   ```

3. **Перевіряйте логи при помилках**
   ```
   logs/test_execution_*.log
   ```

4. **Скріншоти зберігаються при падінні тестів**
   ```
   screenshots/failed_*.png
   ```

## 🚀 Наступні кроки

1. ✅ Запустіть всі тести
2. ✅ Перегляньте звіти
3. ✅ Додайте свій тест
4. ✅ Налаштуйте CI/CD
5. ✅ Інтегруйте з вашим проектом

## 📞 Потрібна допомога?

- Створіть [Issue](https://github.com/VitaliySynytskyi/AQA-Framework/issues)
- Перегляньте [FAQ](README.md)
- Перевірте [Examples](features/)

---

**Готово! Тепер ви можете почати тестування! 🎉**
