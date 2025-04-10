import os
import json
import tempfile
from src.RecipeStorage import RecipeStorage
from src.Recipe import Recipe


class TestRecipeStorage:
    def setup_method(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = os.path.join(self.temp_dir.name, "test_recipes.json")

        # Create empty JSON file
        with open(self.filename, 'w') as f:
            f.write("[]")
        self.original_init = RecipeStorage.__init__

        # Insert the temporary file path into RecipeStorage
        def custom_init(storage_self, _):
            storage_self.filepath = self.filename
            storage_self.recipes = []

        RecipeStorage.__init__ = custom_init

    def teardown_method(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_and_save(self):
        data = {
            "id": "12345abc",
            "source": {
                "title": "Temp Recipe",
                "ingredients": "1x test",
                "steps": "Mix and go",
                "yield": 1
            }
        }
        recipe = Recipe(data)

        storage = RecipeStorage("ignored")
        storage.add(recipe)

        with open(self.filename) as f:
            content = json.load(f)

        assert len(content) == 1
        assert content[0]['id'] == "12345abc"
        assert content[0]['source']['title'] == "Temp Recipe"

    def test_remove_recipe(self):
        # Create two mock recipes
        data_1 = {
            "id": "12345abc",
            "source": {
                "title": "Temp Recipe",
                "ingredients": "1x test",
                "steps": "Mix and go",
                "yield": 1
            }
        }
        recipe_1 = Recipe(data_1)

        data_2 = {
            "id": "67890xyz",
            "source": {
                "title": "Another Recipe",
                "ingredients": "2x test",
                "steps": "Just cook",
                "yield": 2
            }
        }
        recipe_2 = Recipe(data_2)

        # Add both recipes
        storage = RecipeStorage("ignored")
        storage.add(recipe_1)
        storage.add(recipe_2)

        # Check whether both recipes are added
        with open(self.filename) as f:
            content = json.load(f)
        assert len(content) == 2

        # Remove the first recipe (recipe_1)
        storage.remove(recipe_1)

        # Check whether the recipe was removed and only recipe_2 remains
        with open(self.filename) as f:
            content = json.load(f)

        # Only recipe_2 should remain
        assert len(content) == 1
        assert content[0]['id'] == "67890xyz"
        assert content[0]['source']['title'] == "Another Recipe"
