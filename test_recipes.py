import unittest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


class TestIngredient(unittest.TestCase):
    def test_creation(self):
        ing = Ingredient("Греческий йогурт", 200, "г")
        self.assertEqual(ing.name, "Греческий йогурт")
        self.assertEqual(ing.quantity, 200.0)
        self.assertEqual(ing.unit, "г")

    def test_str_and_repr(self):
        ing = Ingredient("Банан", 1, "шт")
        self.assertEqual(str(ing), "Банан: 1.0 шт")
        self.assertEqual(repr(ing), "Ingredient('Банан', 1.0, 'шт')")

    def test_eq(self):
        ing1 = Ingredient("Кокосовое молоко", 200, "мл")
        ing2 = Ingredient("Кокосовое молоко", 100, "мл")
        ing3 = Ingredient("Матча", 200, "мл")
        self.assertEqual(ing1, ing2)
        self.assertNotEqual(ing1, ing3)

    def test_validation(self):
        with self.assertRaises(ValueError):
            Ingredient("Матча", -5, "г")

class TestRecipe(unittest.TestCase):
    def test_add_ingredient_and_len(self):
        recipe = Recipe("Йогурт-боул", [])
        recipe.add_ingredient(Ingredient("Греческий йогурт", 200, "г"))
        recipe.add_ingredient(Ingredient("Банан", 1, "шт"))
        recipe.add_ingredient(Ingredient("Кокосовое молоко", 100, "мл"))
        self.assertEqual(len(recipe), 3)

    def test_summing_duplicates(self):
        recipe = Recipe("Йогурт-боул", [Ingredient("Кокосовое молоко", 100, "мл")])
        recipe.add_ingredient(Ingredient("Кокосовое молоко", 50, "мл"))
        self.assertEqual(recipe.ingredients[0].quantity, 150.0)

    def test_scale(self):
        recipe = Recipe("Матча", [Ingredient("Матча", 5, "г")])
        scaled = recipe.scale(2)
        self.assertEqual(scaled.ingredients[0].quantity, 10.0)
        self.assertEqual(recipe.ingredients[0].quantity, 5.0)

    def test_validation(self):
        with self.assertRaises(TypeError):
            Recipe("Йогурт-боул", None)
        with self.assertRaises(ValueError):
            Recipe("Матча", []).scale(-1)


class TestShoppingList(unittest.TestCase):
    def test_get_list_sums_quantities(self):
        shop = ShoppingList()
        yogurt_bowl = Recipe("Йогурт-боул", [Ingredient("Кокосовое молоко", 200, "мл")])
        matcha = Recipe("Матча", [Ingredient("Кокосовое молоко", 100, "мл")])

        shop.add_recipe(yogurt_bowl, 1)
        shop.add_recipe(matcha, 2)

        final_list = shop.get_list()
        self.assertEqual(len(final_list), 1)
        self.assertEqual(final_list[0].quantity, 400.0)

    def test_remove_recipe(self):
        shop = ShoppingList()
        yogurt_bowl = Recipe("Йогурт-боул", [Ingredient("Банан", 1, "шт")])
        shop.add_recipe(yogurt_bowl, 1)
        shop.remove_recipe("Йогурт-боул")
        self.assertEqual(len(shop.get_list()), 0)

    def test_add_lists(self):
        shop1 = ShoppingList()
        shop1.add_recipe(Recipe("Йогурт-боул", [Ingredient("Банан", 1, "шт")]), 1)
        shop2 = ShoppingList()
        shop2.add_recipe(Recipe("Матча", [Ingredient("Банан", 2, "шт")]), 1)
        combined = shop1 + shop2
        self.assertEqual(combined.get_list()[0].quantity, 3.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            ShoppingList().add_recipe(Recipe("Матча", []), 0)


class TestDietaryRecipe(unittest.TestCase):
    def test_str_and_scale(self):
        rec = DietaryRecipe("Йогурт-боул", "веган", [Ingredient("Гранола", 50, "г")])
        
        rec_str = str(rec)
        self.assertIn("[веган]", rec_str)
        self.assertIn("Йогурт-боул", rec_str)
        self.assertIn("Гранола", rec_str)
        self.assertIn("50.0", rec_str)
        
        scaled = rec.scale(2)
        self.assertIsInstance(scaled, DietaryRecipe)
        self.assertEqual(scaled.diet_type, "веган")
        self.assertEqual(scaled.ingredients[0].quantity, 100.0)


if __name__ == '__main__':
    unittest.main()