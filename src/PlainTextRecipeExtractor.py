import re
from src.RecipeExtractor import RecipeExtractor
from src.RecipeIngredient import RecipeIngredient, INGREDIENT_PATTERN
from src.RecipeStep import RecipeStep


class PlainTextRecipeExtractor(RecipeExtractor):
    def _load(self):
        source = self.get_source()

        # match ingredients
        ingredient_matches = INGREDIENT_PATTERN.findall(source)
        ingredients = [RecipeIngredient(self.recipe, ' '.join(match))
                       for match in ingredient_matches]

        # remove ingredients form text
        source = re.sub(INGREDIENT_PATTERN, '', source)
        lines = source.split('\n')

        # find title (first line longer than 3 chars)
        title_index = None
        for index, line in enumerate(lines):
            if (len(line.strip()) > 3):
                title_index = index
                break

        # steps are all lines longer than 20 chars
        steps = []
        for index, line in enumerate(lines):
            if (index == title_index):
                continue
            if (len(line.strip()) <= 20):
                continue
            steps.append(RecipeStep(self.recipe, line))

        self.extracted_data = {
            'ingredients': ingredients,
            'title': lines[title_index],
            'steps': steps
        }

    def get_yield(self):
        return 4

    def get_steps(self):
        return self.extracted_data['steps']

    def get_title(self):
        return self.extracted_data['title']

    def get_ingredients(self):
        return self.extracted_data['ingredients']
