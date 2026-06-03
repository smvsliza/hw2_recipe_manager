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

# Создаём ингредиенты для йогурт-боула
yogurt = Ingredient("Греческий йогурт", 200, "г")
coconut_milk = Ingredient("Кокосовое молоко", 100, "мл")
banana = Ingredient("Банан", 1, "шт")
granola = Ingredient("Гранола", 50, "г")

# Создаём диетический рецепт йогурт-боула
yogurt_bowl = DietaryRecipe("Йогурт-боул", "веган", [yogurt, coconut_milk, banana])
yogurt_bowl.add_ingredient(granola)
print(yogurt_bowl)

# Создаём рецепт матчи
matcha = Recipe("Матча", [coconut_milk])
matcha.add_ingredient(Ingredient("Матча", 5, "г"))

# Масштабируем матчу на 2 порции
big_matcha = matcha.scale(2)
print(big_matcha)

# Формируем список покупок для обоих рецептов
shopping = ShoppingList()
shopping.add_recipe(yogurt_bowl, portions=1)
shopping.add_recipe(matcha, portions=2)

# Выводим итоговый список (кокосовое молоко просуммируется!)
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