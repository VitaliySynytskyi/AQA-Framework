# AQA Framework - BDD Testing Framework для Rozetka.com.ua

[![CI/CD](https://github.com/VitaliySynytskyi/AQA-Framework/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/VitaliySynytskyi/AQA-Framework/actions/workflows/ci-cd.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📋 Опис проекту

Це комплексний BDD (Behavior-Driven Development) фреймворк для автоматизованого тестування веб-сайту [Rozetka.com.ua](https://rozetka.com.ua). Фреймворк побудований на основі Python, Selenium WebDriver, і Behave, з використанням підходу Page Object Model (POM).

### 🎯 Основні можливості

- ✅ **20+ BDD сценаріїв** написаних на Gherkin
- ✅ **100+ unit-тестів** для покриття функціональності фреймворку
- ✅ **Page Object Model** для легкої підтримки коду
- ✅ **Підтримка декількох браузерів** (Chrome, Firefox, Edge)
- ✅ **CI/CD інтеграція** через GitHub Actions
- ✅ **Allure звіти** для візуалізації результатів
- ✅ **Гнучка конфігурація** через YAML та змінні середовища
- ✅ **Детальне логування** всіх дій

## 🏗️ Архітектура фреймворку

```
AQA Framework/
├── config/                 # Конфігураційні файли
│   └── config.yaml        # Основна конфігурація
├── features/              # BDD feature files
│   ├── environment.py     # Behave environment setup
│   ├── steps/            # Step definitions
│   │   ├── search_steps.py
│   │   ├── sorting_steps.py
│   │   ├── navigation_steps.py
│   │   ├── language_steps.py
│   │   └── cart_steps.py
│   ├── search.feature    # Сценарії пошуку
│   ├── sorting.feature   # Сценарії сортування
│   ├── navigation.feature # Сценарії навігації
│   ├── language.feature  # Сценарії зміни мови
│   └── cart.feature      # Сценарії кошика
├── framework/             # Ядро фреймворку
│   ├── browser_manager.py # Керування браузером
│   ├── config_manager.py  # Керування конфігурацією
│   └── logger.py          # Система логування
├── pages/                 # Page Objects
│   ├── base_page.py      # Базовий клас
│   ├── home_page.py      # Головна сторінка
│   ├── search_page.py    # Сторінка пошуку
│   ├── cart_page.py      # Сторінка кошика
│   └── category_page.py  # Сторінка категорії
├── unit_tests/           # Unit тести
│   ├── test_config_manager.py
│   ├── test_browser_manager.py
│   ├── test_base_page.py
│   ├── test_home_page.py
│   ├── test_search_page.py
│   ├── test_cart_page.py
│   └── test_category_page.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # CI/CD pipeline
├── requirements.txt       # Python залежності
├── behave.ini            # Behave конфігурація
├── pytest.ini            # Pytest конфігурація
└── README.md             # Документація

```

## 🚀 Початок роботи

### Передумови

- Python 3.9 або вище
- pip (Python package manager)
- Git

### Встановлення

1. **Клонуйте репозиторій:**
```bash
git clone https://github.com/VitaliySynytskyi/AQA-Framework.git
cd "AQA Framework"
```

2. **Створіть віртуальне середовище:**
```bash
python -m venv venv
```

3. **Активуйте віртуальне середовище:**
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Встановіть залежності:**
```bash
pip install -r requirements.txt
```

5. **Створіть файл .env (опціонально):**
```bash
copy .env.example .env
```

## 🧪 Запуск тестів

### BDD тести (Behave)

**Запустити всі BDD тести:**
```bash
behave features/
```

**Запустити конкретну feature:**
```bash
behave features/search.feature
```

**Запустити з Allure звітами:**
```bash
behave features/ --format allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

**Запустити в headless режимі:**
```bash
set HEADLESS=true
behave features/
```

### Unit тести (Pytest)

**Запустити всі unit тести:**
```bash
pytest unit_tests/ -v
```

**Запустити з покриттям коду:**
```bash
pytest unit_tests/ -v --cov=. --cov-report=html
```

**Запустити конкретний тестовий файл:**
```bash
pytest unit_tests/test_home_page.py -v
```

**Відкрити звіт покриття:**
```bash
start htmlcov/index.html
```

## ⚙️ Конфігурація

### config/config.yaml

```yaml
browser:
  name: chrome          # chrome, firefox, edge
  headless: false       # true для headless режиму
  window_size: 1920x1080

site:
  base_url: https://rozetka.com.ua
  supported_languages:
    - uk
    - ru

timeouts:
  short: 5
  medium: 10
  long: 30
```

### Змінні середовища (.env)

```env
BASE_URL=https://rozetka.com.ua
BROWSER=chrome
HEADLESS=false
IMPLICIT_WAIT=10
PAGE_LOAD_TIMEOUT=30
```

## 📊 BDD Тестові сценарії

### 1. Пошук товарів (search.feature)
- ✅ Успішний пошук з валідним запитом
- ✅ Пошук конкретного товару
- ✅ Пошук з порожнім запитом
- ✅ Пошук неіснуючого товару
- ✅ Пошук через Enter
- ✅ Багатомовний пошук

### 2. Сортування (sorting.feature)
- ✅ Сортування за ціною (зростання/спадання)
- ✅ Сортування за популярністю
- ✅ Сортування за новинками
- ✅ Збереження сортування після оновлення

### 3. Навігація (navigation.feature)
- ✅ Відкриття каталогу
- ✅ Перехід до категорії
- ✅ Навігація по breadcrumbs
- ✅ Повернення на головну

### 4. Зміна мови (language.feature)
- ✅ Перемикання на українську
- ✅ Перемикання на російську
- ✅ Збереження мови після навігації

### 5. Кошик (cart.feature)
- ✅ Додавання товару до кошика
- ✅ Видалення товару з кошика
- ✅ Зміна кількості товару
- ✅ Перевірка вмісту кошика

## 🧩 Page Object Model

### BasePage
Базовий клас з загальними методами:
- `find_element()` - пошук елемента з очікуванням
- `click()` - клік з очікуванням кліккабельності
- `input_text()` - введення тексту
- `is_element_visible()` - перевірка видимості
- `take_screenshot()` - створення скріншоту

### Спеціалізовані сторінки
- **HomePage** - головна сторінка (пошук, каталог, мова)
- **SearchPage** - результати пошуку (сортування, фільтри)
- **CartPage** - кошик (управління товарами)
- **CategoryPage** - категорія товарів (навігація, підкатегорії)

## 📈 CI/CD Pipeline

GitHub Actions автоматично запускає:
1. **Unit тести** на Python 3.9, 3.10, 3.11
2. **BDD тести** з генерацією Allure звітів
3. **Linting** (flake8, black)
4. **Security scan** (bandit)
5. **Code coverage** звіти

Результати публікуються на GitHub Pages.

## 📝 Додавання нових тестів

### Додавання BDD сценарію

1. Створіть новий .feature файл або додайте сценарій:
```gherkin
Scenario: New test scenario
  Given I am on the home page
  When I perform some action
  Then I should see expected result
```

2. Створіть step definitions у файлі steps/:
```python
@when('I perform some action')
def step_impl(context):
    # Ваш код
    pass
```

### Додавання unit тесту

```python
def test_new_functionality(self, mock_driver):
    """Test description"""
    page = HomePage(mock_driver)
    result = page.some_method()
    assert result == expected_value
```

## 🤝 Внесок у проект

1. Fork репозиторій
2. Створіть feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit зміни (`git commit -m 'Add some AmazingFeature'`)
4. Push до branch (`git push origin feature/AmazingFeature`)
5. Створіть Pull Request

## 📄 Ліцензія

Цей проект ліцензовано під MIT License.

## 👨‍💻 Автор

**Vitaliy Synytskyi**
- GitHub: [@VitaliySynytskyi](https://github.com/VitaliySynytskyi)

## 📞 Підтримка

Якщо у вас є питання або проблеми, створіть [Issue](https://github.com/VitaliySynytskyi/AQA-Framework/issues).

---

**⭐ Якщо цей проект був корисним, поставте зірку!**
