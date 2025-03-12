from RecipeExtractor import RecipeExtractor
from PlainTextRecipeExtractor import PlainTextRecipeExtractor
from bs4 import BeautifulSoup
import argparse
import re
import json
from RecipeIngredient import RecipeIngredient
from RecipeStep import RecipeStep
import utils

# pattern for invalid ingredients
INGREDIENT_INVALID_PATTERN = re.compile(r'[\[\]]')

def is_recipe_instruction(str):
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
            isinstance(value[0], dict) and 
            value[0]['@type'] == 'HowToStep')

class LinkedDataRecipeExtractor(RecipeExtractor):
    def __init__(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        
        # Extract recipe linked data
        ld_tag = self.soup.find('script', type='application/ld+json', string=re.compile(r'"@type":\s*"Recipe"'))
        if ld_tag: 
            ld = json.loads(ld_tag.text, strict=False)
            self.ld = utils.loop_recursive(ld, is_ld_recipe_node)
    
    def get_name(self):
        if(self.ld['name']): return self.ld['name']

    def get_steps(self):
        """Extract how-to steps from `self.ld`."""
        ld_steps = utils.loop_recursive(self.ld, is_ld_steps_node)
        if(ld_steps):       
            return [RecipeStep.from_linked_data(ld_step) for ld_step in ld_steps]
        
        if('recipeInstructions' in self.ld):
            instructions = self.ld['recipeInstructions'].split('\n')
            return [RecipeStep.from_str(i) 
                for i in instructions if is_recipe_instruction(i)]
    
    def get_ingredients(self):
        ingredient_strs = self.ld['recipeIngredient']
        
        ingredients = [RecipeIngredient.from_str(str) for str in ingredient_strs]
        valid_ingredients = [i for i in ingredients if i.is_valid()]
        if(len(valid_ingredients) > 0): return valid_ingredients
        
        # fallback to plain text extraction if not all ingredients were valid
        ingredients_element = self.soup.find(class_=re.compile(r'print-ingredients_root'))
        
        text = ingredients_element.get_text()
        extractor = PlainTextRecipeExtractor(text)
        return extractor.get_ingredients()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='path to HTML input file.')
    parser.add_argument('-m', '--mod', 
        help='ingredients modifier.', default='1')
    args = parser.parse_args()
    
    with open(args.filename, encoding='utf8') as file:
        html_doc = file.read()
        extractor = LinkedDataRecipeExtractor(html_doc)
        
        print()
        print(extractor.get_name())
        print()
        
        print('Steps:')
        for i, step in enumerate(extractor.get_steps()):
            print(f'- {step.get_text()}')
        print()
        
        print('Ingredients:')
        for ingredient in extractor.get_ingredients():
            print(f'- {ingredient.get_multiplied_text(float(args.mod))}')
        print()
    
   
if __name__ == '__main__':
    main()