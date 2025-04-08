from src.RecipeExtractor import RecipeExtractor
from src.RecipeIngredient import RecipeIngredient, INGREDIENT_PATTERN
from src.RecipeStep import RecipeStep


class JSONRecipeExtractor(RecipeExtractor):
    def _load(self):
        self.data = self.get_source()

    @staticmethod
    def accepts(recipe):
        return 'title' in recipe.get_source()

    def get_yield(self):
        if 'yield' not in self.data:
            return 4
        return self.data['yield']

    def get_steps(self):
        steps = self.data['steps'].split('\n')
        return [RecipeStep(self.recipe, s) for s in steps if len(s)]

    def get_title(self):
        return self.data['title']

    def get_ingredients(self):
        ingredients = self.data['ingredients'].split('\n')
        return [RecipeIngredient(self.recipe, s)
                for s in ingredients if len(s)]
