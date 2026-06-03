class Ingredient:

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
    def __init__(self, title: str, ingredients: list):
        if not isinstance(ingredients, list):
            raise TypeError("ingredients должен быть списком объектов Ingredient")
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient: Ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        return type(ratio) in (int, float) and ratio > 0

    def scale(self, ratio: float) -> 'Recipe':
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэф. должен быть положительным числом")
        
        new_ingredients = [
            Ingredient(i.name, i.quantity*ratio, i.unit)
            for i in self.ingredients
        ]
        return Recipe(self.title, new_ingredients)

    def __len__(self) -> int:
        return len(self.ingredients)

    def __str__(self) -> str:
        ingredients = "\n".join(f"{ingr}" for ingr in self.ingredients)
        return f"Рецепт: {self.title}\n{ingredients}"
    

class ShoppingList:

    def __init__(self):
        self._items = []

    @staticmethod
    def _get_name(ingredient):
        return ingredient.name

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled = recipe.scale(portions)
        for ingr in scaled.ingredients:
            self._items.append((ingr, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [
            (ingr, rec_title) 
            for ingr, rec_title in self._items 
            if rec_title != title
        ]

    def get_list(self) -> list:
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