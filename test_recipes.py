import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


class TestIngredient:
    def test_creation(self):
        ing = Ingredient("Греческий йогурт", 200, "г")
        assert ing.name == "Греческий йогурт"
        assert ing.quantity == 200.0
        assert ing.unit == "г"

    def test_str_and_repr(self):
        ing = Ingredient("Банан", 1, "шт")
        assert str(ing) == "Банан: 1.0 шт"
        assert repr(ing) == "Ingredient('Банан', 1.0, 'шт')"

    def test_eq(self):
        ing1 = Ingredient("Кокосовое молоко", 200, "мл")
        ing2 = Ingredient("Кокосовое молоко", 100, "мл")
        ing3 = Ingredient("Матча", 200, "мл")
        assert ing1 == ing2
        assert ing1 != ing3

    def test_validation(self):
        with pytest.raises(ValueError):
            Ingredient("Матча", -5, "г")


class TestRecipe:
    def test_add_ingredient_and_len(self):
        recipe = Recipe("Йогурт-боул", [])
        recipe.add_ingredient(Ingredient("Греческий йогурт", 200, "г"))
        recipe.add_ingredient(Ingredient("Банан", 1, "шт"))
        recipe.add_ingredient(Ingredient("Кокосовое молоко", 100, "мл"))
        assert len(recipe) == 3

    def test_summing_duplicates(self):
        recipe = Recipe("Йогурт-боул", [Ingredient("Кокосовое молоко", 100, "мл")])
        recipe.add_ingredient(Ingredient("Кокосовое молоко", 50, "мл"))
        assert recipe.ingredients[0].quantity == 150.0

    def test_scale(self):
        recipe = Recipe("Матча", [Ingredient("Матча", 5, "г")])
        scaled = recipe.scale(2)
        assert scaled.ingredients[0].quantity == 10.0
        assert recipe.ingredients[0].quantity == 5.0

    def test_validation(self):
        with pytest.raises(TypeError):
            Recipe("Йогурт-боул", None)
        with pytest.raises(ValueError):
            Recipe("Матча", []).scale(-1)


class TestShoppingList:
    def test_get_list_sums_quantities(self):
        shop = ShoppingList()
        yogurt_bowl = Recipe("Йогурт-боул", [Ingredient("Кокосовое молоко", 200, "мл")])
        matcha = Recipe("Матча", [Ingredient("Кокосовое молоко", 100, "мл")])
        shop.add_recipe(yogurt_bowl, 1)
        shop.add_recipe(matcha, 2)
        final_list = shop.get_list()
        assert len(final_list) == 1
        assert final_list[0].quantity == 400.0

    def test_remove_recipe(self):
        shop = ShoppingList()
        yogurt_bowl = Recipe("Йогурт-боул", [Ingredient("Банан", 1, "шт")])
        shop.add_recipe(yogurt_bowl, 1)
        shop.remove_recipe("Йогурт-боул")
        assert len(shop.get_list()) == 0

    def test_add_lists(self):
        shop1 = ShoppingList()
        shop1.add_recipe(Recipe("Йогурт-боул", [Ingredient("Банан", 1, "шт")]), 1)
        shop2 = ShoppingList()
        shop2.add_recipe(Recipe("Матча", [Ingredient("Банан", 2, "шт")]), 1)
        combined = shop1 + shop2
        assert combined.get_list()[0].quantity == 3.0

    def test_validation(self):
        with pytest.raises(ValueError):
            ShoppingList().add_recipe(Recipe("Матча", []), 0)


class TestDietaryRecipe:
    def test_str_and_scale(self):
        rec = DietaryRecipe("Йогурт-боул", "веган", [Ingredient("Гранола", 50, "г")])
        rec_str = str(rec)
        assert "[веган]" in rec_str
        assert "Йогурт-боул" in rec_str
        assert "Гранола" in rec_str
        assert "50.0" in rec_str
        scaled = rec.scale(2)
        assert isinstance(scaled, DietaryRecipe)
        assert scaled.diet_type == "веган"
        assert scaled.ingredients[0].quantity == 100.0