from RecipeExtractor import RecipeExtractor
from bs4 import BeautifulSoup
import argparse
import re
import json
from RecipeIngredient import RecipeIngredient, INGREDIENT_PATTERN
import utils

class PlainTextRecipeExtractor(RecipeExtractor):
    def __init__(self, text):
        self.text = text

    def get_steps(self):
        pass
    
    def get_ingredients(self):
        ingredient_matches = INGREDIENT_PATTERN.findall(self.text)
        return [RecipeIngredient.from_str(' '.join(m)) 
            for m in ingredient_matches]
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    
    with open(args.filename, encoding='utf8') as file:
        html_doc = file.read()
        extractor = PlainTextRecipeExtractor(html_doc)
        
        print('Name: ', end='')
        print(extractor.get_name())
        print()
        
        print('Steps:')
        print(extractor.get_steps())
        
        print('Ingredients:')
        print(extractor.get_ingredients())
    
   
if __name__ == '__main__':
    main()