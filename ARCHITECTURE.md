# AQA Framework - Архітектура та Дизайн

## Огляд архітектури

Фреймворк побудований на принципах модульності, розширюваності та підтримуваності.

## Основні компоненти

### 1. Framework Layer (Ядро фреймворку)

#### ConfigManager (`framework/config_manager.py`)
- **Призначення**: Централізоване керування конфігурацією
- **Патерн**: Singleton
- **Функції**:
  - Завантаження конфігурації з YAML
  - Перевизначення через змінні середовища
  - Доступ до конфігурації через dot-notation

#### BrowserManager (`framework/browser_manager.py`)
- **Призначення**: Керування життєвим циклом браузера
- **Підтримувані браузери**: Chrome, Firefox, Edge
- **Функції**:
  - Ініціалізація WebDriver з опціями
  - Налаштування timeouts та window size
  - Headless режим
  - Автоматична установка драйверів (webdriver-manager)

#### Logger (`framework/logger.py`)
- **Призначення**: Централізоване логування
- **Особливості**:
  - Кольорове виведення в консоль
  - Запис у файл з ротацією
  - Різні рівні логування (DEBUG, INFO, WARNING, ERROR)

### 2. Page Object Layer (Шар об'єктів сторінок)

#### BasePage (`pages/base_page.py`)
- **Призначення**: Базовий клас для всіх page objects
- **Ключові методи**:
  ```python
  find_element(locator, timeout)      # Пошук елемента з очікуванням
  click(locator, timeout)             # Клік з очікуванням
  input_text(locator, text)           # Введення тексту
  get_text(locator)                   # Отримання тексту
  is_element_visible(locator)         # Перевірка видимості
  scroll_to_element(locator)          # Прокрутка до елемента
  take_screenshot(name)               # Створення скріншоту
  execute_script(script)              # Виконання JavaScript
  ```

#### Спеціалізовані Page Objects

**HomePage** (`pages/home_page.py`)
- Пошук товарів
- Відкриття каталогу
- Зміна мови
- Перехід до кошика

**SearchPage** (`pages/search_page.py`)
- Перегляд результатів пошуку
- Сортування товарів
- Фільтрація за ціною
- Додавання до кошика

**CartPage** (`pages/cart_page.py`)
- Перегляд вмісту кошика
- Зміна кількості товарів
- Видалення товарів
- Оформлення замовлення

**CategoryPage** (`pages/category_page.py`)
- Навігація по категоріях
- Перегляд підкатегорій
- Breadcrumbs навігація

### 3. BDD Test Layer (Шар BDD тестів)

#### Feature Files (`features/*.feature`)
Написані на Gherkin DSL:
```gherkin
Feature: Product Search
  Scenario: Successful product search
    Given I am on the Rozetka home page
    When I search for "laptop"
    Then I should see search results
```

#### Step Definitions (`features/steps/*_steps.py`)
Реалізація кроків у Python:
```python
@when('I search for "{query}"')
def step_search_for_product(context, query):
    context.home_page.search_product(query)
```

#### Environment (`features/environment.py`)
- Hooks для setup/teardown
- Ініціалізація browser та page objects
- Обробка помилок та скріншоти

### 4. Unit Test Layer (Шар unit тестів)

#### Test Structure (`unit_tests/test_*.py`)
```python
class TestHomePage:
    @pytest.fixture
    def home_page(self, mock_driver):
        return HomePage(mock_driver)
    
    def test_search_product(self, home_page):
        # Test implementation
```

## Патерни проектування

### 1. Page Object Model (POM)
- Інкапсуляція логіки сторінки
- Розділення тестів та коду взаємодії з UI
- Легка підтримка при змінах UI

### 2. Singleton
- ConfigManager має єдиний екземпляр
- Забезпечує консистентність конфігурації

### 3. Factory Pattern
- BrowserManager створює різні типи браузерів
- Легко додати підтримку нових браузерів

### 4. Template Method
- BasePage визначає загальні методи
- Дочірні класи використовують та розширюють

## Потік виконання тесту

```
1. Behave запускає feature файл
   ↓
2. environment.py виконує before_scenario
   ↓
3. BrowserManager створює WebDriver
   ↓
4. Ініціалізуються Page Objects
   ↓
5. Step definitions викликають методи Page Objects
   ↓
6. Page Objects взаємодіють з WebDriver
   ↓
7. Перевірки (assertions) в step definitions
   ↓
8. environment.py виконує after_scenario
   ↓
9. BrowserManager закриває браузер
   ↓
10. Генеруються звіти
```

## Розширюваність

### Додавання нового браузера

```python
# В browser_manager.py
def _start_safari(self) -> webdriver.Safari:
    options = SafariOptions()
    # Configure options
    return webdriver.Safari(options=options)

def start_browser(self):
    if browser_name == 'safari':
        self.driver = self._start_safari()
```

### Додавання нової Page Object

```python
# pages/product_page.py
from pages.base_page import BasePage

class ProductPage(BasePage):
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product-title")
    
    def get_product_title(self):
        return self.get_text(self.PRODUCT_TITLE)
```

### Додавання нового BDD сценарію

```gherkin
# features/new_feature.feature
Feature: New Feature
  Scenario: New scenario
    Given preconditions
    When action
    Then expected result
```

```python
# features/steps/new_steps.py
@given('preconditions')
def step_impl(context):
    # Implementation
```

## Best Practices

1. **Separation of Concerns**
   - UI логіка в Page Objects
   - Бізнес-логіка в step definitions
   - Конфігурація окремо

2. **DRY (Don't Repeat Yourself)**
   - Загальні методи в BasePage
   - Reusable step definitions
   - Shared fixtures

3. **Explicit Waits**
   - Завжди використовуйте explicit waits
   - Уникайте time.sleep()
   - Налаштовуйте timeouts через конфігурацію

4. **Clear Naming**
   - Описові назви методів
   - Зрозумілі locators
   - Readable Gherkin scenarios

5. **Error Handling**
   - Graceful degradation
   - Meaningful error messages
   - Screenshots on failure

## Залежності

```
selenium - WebDriver для браузерної автоматизації
behave - BDD framework
pytest - Unit testing framework
allure-behave - Reporting
webdriver-manager - Автоматична установка драйверів
pyyaml - Парсинг конфігурації
colorlog - Кольорове логування
```

## Майбутні покращення

1. API тестування
2. Підтримка мобільних браузерів
3. Parallel execution для BDD
4. Docker контейнеризація
5. Integration з Test Management системами
6. Performance тестування
7. Visual regression testing
8. Database testing capabilities
