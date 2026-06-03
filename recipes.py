"""Модуль с классами для управления рецептами."""

class Ingredient:
    """Представляет отдельный продукт или компонент блюда."""

    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit
    

class Recipe:
    """Представляет рецепт одного блюда."""
    def __init__(self, title: str, ingredients: list):
        if not isinstance(ingredients, list):
            raise TypeError("ingredients должен быть списком объектов Ingredient")
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient: Ingredient):
        """Добавляет ингредиент. Если такой уже есть, суммирует количество."""
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        """Проверяет, что ratio — число и больше нуля."""
        return type(ratio) in (int, float) and ratio > 0

    def scale(self, ratio: float) -> 'Recipe':
        """Возвращает новый масштабированный рецепт. Исходный не меняется."""
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэф. должен быть положительным числом")
        
        new_ingredients = [
            Ingredient(i.name, i.quantity*ratio, i.unit)
            for i in self.ingredients
        ]
        return Recipe(self.title, new_ingredients)

    def __len__(self) -> int:
        """Возвращает количество уникальных ингредиентов."""
        return len(self.ingredients)

    def __str__(self) -> str:
        """Возвращает читаемое представление рецепта."""
        ingredients = "\n".join(f"{ingr}" for ingr in self.ingredients)
        return f"Рецепт: {self.title}\n{ingredients}"
    

class ShoppingList:
    """Представляет список покупок, объединяющий ингредиенты из нескольких рецептов."""

    def __init__(self):
        self._items = []

    @staticmethod
    def _get_name(ingredient):
        """Вспомогательная функция для сортировки по названию ингредиента."""
        return ingredient.name

    def add_recipe(self, recipe: Recipe, portions: float):
        """Добавляет масштабированный рецепт в список покупок."""
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled = recipe.scale(portions)
        for ingr in scaled.ingredients:
            self._items.append((ingr, recipe.title))

    def remove_recipe(self, title: str):
        """Удаляет все ингредиенты, относящиеся к рецепту с указанным названием."""
        self._items = [
            (ingr, rec_title) 
            for ingr, rec_title in self._items 
            if rec_title != title
        ]

    def get_list(self) -> list:
        """Возвращает итоговый отсортированный список ингредиентов."""
        totals = {}
        for ingr, _ in self._items:
            key = (ingr.name, ingr.unit)
            if key in totals:
                totals[key] += ingr.quantity
            else:
                totals[key] = ingr.quantity
        
        result = [
            Ingredient(name, quantity, unit)
            for (name, unit), quantity in totals.items()
        ]
        
        result.sort(key=ShoppingList._get_name)
        return result

    def __add__(self, other: 'ShoppingList') -> 'ShoppingList':
        """Объединяет два списка покупок, не изменяя исходные."""
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
    

class DietaryRecipe(Recipe):

    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        if ingredients is None:
            ingredients = []
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float) -> 'DietaryRecipe':
        scaled = super().scale(ratio)
        return DietaryRecipe(scaled.title, self.diet_type, scaled.ingredients)

    def __str__(self) -> str:
        return f"[{self.diet_type}] {super().__str__()}"