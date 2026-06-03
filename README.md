# Recipe Manager

Домашнее задание написано в рамках курса «Технологии программирования» (НИУ ВШЭ, БИ)

Приложение для управления рецептами: позволяет описывать ингредиенты, собирать из них рецепты блюд, масштабировать порции и автоматически формировать сводный список покупок сразу для нескольких рецептов.

## Структура проекта

```
.
├── recipes.py         # классы Ingredient, Recipe, DietaryRecipe, ShoppingList
├── test_recipes.py    # тесты на pytest
├── requirements.txt   # зафиксированные зависимости проекта
├── .gitignore
└── README.md
```

Основные классы:

- `Ingredient` — отдельный продукт: название, количество, единица измерения. Количество реализовано через `@property` с валидацией.
- `Recipe` — рецепт блюда: название и список ингредиентов. Умеет добавлять ингредиенты без дубликатов и масштабировать порции методом `scale`.
- `DietaryRecipe` — наследник `Recipe` с дополнительной диетической категорией (например, «веган», «без глютена»).
- `ShoppingList` — список покупок, собирающий ингредиенты из нескольких рецептов и суммирующий одинаковые позиции.

## Установка

Проект разворачивается из чистого клона репозитория следующими командами:

```bash
git clone https://github.com/smvliza/hw2_recipe_manager.git
cd hw2_recipe_manager
python -m venv venv
source venv/bin/activate        # для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Требуется Python 3.10 или новее.

## Использование

### Запуск кода

Классы можно импортировать из модуля `recipes.py` и использовать в своём скрипте или интерактивной сессии Python:

```python
from recipes import Ingredient, Recipe, DietaryRecipe, ShoppingList

# Создаём ингредиенты
flour = Ingredient("Мука", 500, "г")
eggs = Ingredient("Яйца", 2, "шт")

# Собираем рецепт
pancakes = Recipe("Блины", [flour, eggs])
pancakes.add_ingredient(Ingredient("Молоко", 500, "мл"))

# Масштабируем на 3 порции
big_batch = pancakes.scale(3)
print(big_batch)

# Формируем список покупок
shopping = ShoppingList()
shopping.add_recipe(pancakes, portions=2)
for item in shopping.get_list():
    print(item)
```

### Запуск тестов

Тесты написаны с использованием `pytest`. Из корня проекта:

```bash
pytest
```

Или с помощью внутреннего встроенного тестирования:

```bash
python -m unittest test_recipes.py
```

## Автор
Волкова Елизавета, ББИ2509, НИУ ВШЭ, ВШБ БИ