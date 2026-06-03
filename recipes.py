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