from src.PlainTextRecipeExtractor import PlainTextRecipeExtractor
from src.RecipeExtractor import RecipeExtractor
from bs4 import BeautifulSoup
import re
import json
from src.RecipeIngredient import RecipeIngredient
from src.RecipeStep import RecipeStep
import src.utils as utils


def is_recipe_step(str):
    """
    Check `str` is a recipe instruction, or if it's more likely
    to be a heading of some sort.
    """
    str = str.strip()
    return len(str) > 2 and ' ' in str


def is_ld_recipe_node(value):
    """
    Check if `value` is the {"@type":"Recipe"} LD-dictionary.
    """
    return isinstance(value, dict) and value.get('@type') == 'Recipe'


def is_ld_steps_node(value):
    """
    Check if `value` is the [{"@type":"HowToStep"}] LD-list.
    """
    return (isinstance(value, list) and
            len(value) > 0 and
            isinstance(value[0], dict) and
            value[0]['@type'] == 'HowToStep')


class LinkedDataRecipeExtractor(RecipeExtractor):
    def _load(self):
        self.soup = BeautifulSoup(self.get_source(), 'html.parser')

        # Extract recipe linked data
        ld_tag = self.soup.find(
            'script', type='application/ld+json',
            string=re.compile(r'"@type":\s*"Recipe"'))
        if ld_tag:
            ld = json.loads(ld_tag.text, strict=False)
            self.ld = utils.loop_recursive(ld, is_ld_recipe_node)

    @staticmethod
    def accepts(recipe):
        return 'application/ld+json' in recipe.get_source()

    def get_title(self):
        if (self.ld['name']):
            return self.ld['name']

    def get_steps(self):
        """Extract how-to steps from `self.ld`."""
        ld_steps = utils.loop_recursive(self.ld, is_ld_steps_node)
        if (ld_steps):
            return [RecipeStep(self.recipe, ld_step['text'].strip())
                    for ld_step in ld_steps]

        if ('recipeInstructions' in self.ld):
            steps = self.ld['recipeInstructions'].split('\n')
            return [RecipeStep(self.recipe, s)
                    for s in steps if is_recipe_step(s)]

    def get_yield(self):
        if 'recipeYield' in self.ld:
            match = re.search('([0-9]+)', str(self.ld['recipeYield']))
            if (len(match.groups())):
                return int(match.groups()[0])

        return 4

    def get_ingredients(self):
        ingredient_strs = self.ld['recipeIngredient']

        ingredients = [RecipeIngredient(self.recipe, str)
                       for str in ingredient_strs]
        valid_ingredients = [i for i in ingredients if i.is_valid()]
        if (len(valid_ingredients) > 0):
            return valid_ingredients

        # fallback to plain text extraction if not all ingredients are valid
        ingredients_element = self.soup.find(
            class_=re.compile(r'print-ingredients_root'))

        text = ingredients_element.get_text()
        extractor = PlainTextRecipeExtractor(self.recipe, text)
        return extractor.get_ingredients()
