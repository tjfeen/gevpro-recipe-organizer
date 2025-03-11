from RecipeExtractor import RecipeExtractor
from bs4 import BeautifulSoup
import argparse
import re
import json

class HTMLRecipeExtractor(RecipeExtractor):
    def __init__(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')

    def _get_steps_json(self):
        """Get recipe steps from the JSON data on the page."""
        json_tag = self.soup.find('script', type='application/ld+json')
        if not json_tag: return
        
        recipe_data = json.loads(json_tag.text)
        print(recipe_data)

    def get_steps(self):
        json_steps = self._get_steps_json()
        number_tags = self.soup.find_all(string=re.compile(r'[0-9]'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    
    with open(args.filename, encoding='utf8') as file:
        html_doc = file.read()
        extractor = HTMLRecipeExtractor(html_doc)
        
        print('Steps:')
        print(extractor.get_steps())
        
        # print('Ingredients:')
        # print(extractor.get_ingredients())
    
   
if __name__ == '__main__':
    main()