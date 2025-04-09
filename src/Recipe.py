from src.LinkedDataRecipeExtractor import LinkedDataRecipeExtractor
from src.PlainTextRecipeExtractor import PlainTextRecipeExtractor
from src.JSONRecipeExtractor import JSONRecipeExtractor
import random
import json
import argparse


class Recipe:
    def __init__(self, data):
        if 'id' not in data:
            # set recipe id to random hex string
            data['id'] = format(random.getrandbits(64), f'0{64 // 4}x')

        self.data = data
        self.extractor = self._find_extractor()

    def _find_extractor(self):
        """Find the best data extractor for this recipe."""
        if LinkedDataRecipeExtractor.accepts(self):
            return LinkedDataRecipeExtractor(self)

        if (JSONRecipeExtractor.accepts(self)):
            return JSONRecipeExtractor(self)

        return PlainTextRecipeExtractor(self)

    def get_source(self):
        """Get the source data of the recipe."""
        return self.data['source']

    def get_title(self):
        """Get the title of the recipe."""
        return self.extractor.get_title()

    def get_steps(self):
        """Get the how-to steps of the recipe."""
        return self.extractor.get_steps()

    def get_ingredients(self):
        """Get the ingredients needed for the recipe."""
        return self.extractor.get_ingredients()

    def get_id(self):
        return self.data['id']

    def get_rating(self):
        if 'rating' not in self.data:
            return 0
        return self.data['rating']

    def set_rating(self, rating):
        self.data['rating'] = rating

    def serialize(self):
        return self.data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='path to HTML input file')
    parser.add_argument('-p', '--people',
                        help='the number of people to base the recipe on',
                        default='2')
    args = parser.parse_args()

    with open(args.filename, encoding='utf8') as file:
        html_doc = file.read()
        recipe = Recipe(html_doc)

        print()
        print(recipe.get_title())
        print(f'    for {args.people} people, use `-p N` to modify.')
        print()

        print('Steps:')
        for i, step in enumerate(recipe.get_steps()):
            prefix = f'{(f"{i + 1})"):<3}'
            print(f'{prefix} {step.get_text()}')
        print()

        recipe_yield = recipe.extractor.get_yield()
        yield_modifier = int(args.people) / recipe_yield
        print(f'Ingredients:')
        for ingredient in recipe.get_ingredients():
            print(f'- {ingredient.get_text(int(args.people))}')
        print()


if __name__ == '__main__':
    main()
