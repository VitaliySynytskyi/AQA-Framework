# Правильні селектори для кошика Rozetka (2025)

## Перевірені та робочі селектори

### Основні елементи кошика

```python
# Модальне вікно кошика
CART_MODAL = (By.CSS_SELECTOR, "rz-modal")

# Елементи товарів у кошику
CART_ITEMS = (By.CSS_SELECTOR, "rz-cart-product")

# Назви товарів
CART_ITEM_TITLES = (By.CSS_SELECTOR, ".cart-product__title")

# Поле вводу кількості
CART_ITEM_QUANTITIES = (By.CSS_SELECTOR, "rz-cart-product input[formcontrolname='quantity']")
```

### Кнопки керування кількістю

**Збільшити кількість (кнопка +):**
```python
QUANTITY_INCREASE_BUTTONS = (By.CSS_SELECTOR, "rz-cart-counter > div > button:nth-child(3)")
```

**Зменшити кількість (кнопка -):**
```python
QUANTITY_DECREASE_BUTTONS = (By.CSS_SELECTOR, "rz-cart-counter > div > button:nth-child(1)")
```

### Видалення товару з кошика

**Крок 1: Відкрити меню дій товару**
```python
# Знайти кнопку меню для конкретного товару
CART_ITEM_ACTION_MENU = (By.CSS_SELECTOR, "button[id^='cartProductActions']")
```

**Крок 2: Натиснути кнопку видалення в меню**
```python
# Після відкриття меню, знайти кнопку видалення
REMOVE_ITEM_BUTTON_IN_MENU = (By.CSS_SELECTOR, "rz-trash-icon > button")
```

### Повідомлення про порожній кошик

```python
EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".cart-dummy__content, .cart-dummy")
```

### Кнопка "Продовжити покупки"

```python
CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "a.cart-dummy__button, button.cart-dummy__button")
```

## Приклад використання

### Видалення товару з кошика

```python
def remove_item(self, index: int = 0):
    # 1. Знайти всі товари в кошику
    cart_items = self.find_elements((By.CSS_SELECTOR, "rz-cart-product"))
    
    # 2. Вибрати потрібний товар
    cart_item = cart_items[index]
    
    # 3. Знайти кнопку меню дій для цього товару
    action_menu = cart_item.find_element(By.CSS_SELECTOR, "button[id^='cartProductActions']")
    action_menu.click()
    
    # 4. Знайти та натиснути кнопку видалення
    remove_button = cart_item.find_element(By.CSS_SELECTOR, "rz-trash-icon > button")
    remove_button.click()
```

### Збільшення кількості товару

```python
def increase_quantity(self, index: int = 0):
    # Знайти всі кнопки "+"
    increase_buttons = self.find_elements((By.CSS_SELECTOR, "rz-cart-counter > div > button:nth-child(3)"))
    
    # Натиснути потрібну кнопку
    increase_buttons[index].click()
```

## Важливі примітки

1. **Кнопки +/- завжди присутні** у кошику для зміни кількості
2. **Видалення товару** вимагає два кроки: відкрити меню → натиснути видалення
3. **Селектор nth-child(3)** - це кнопка "+", **nth-child(1)** - це кнопка "-"
4. **ID меню дій** починається з `cartProductActions` і має номер (наприклад, `cartProductActions0`)

## Оновлення (листопад 2024)

Всі селектори перевірені та працюють з поточною версією сайту Rozetka.com.ua
