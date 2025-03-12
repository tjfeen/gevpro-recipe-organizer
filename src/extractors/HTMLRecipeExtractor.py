from RecipeExtractor import RecipeExtractor
from bs4 import BeautifulSoup
import argparse
import re
import json

class HTMLRecipeExtractor(RecipeExtractor):
    def __init__(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        
        # Extract recipe linking data
        ld_tag = self.soup.find('script', type='application/ld+json', string=re.compile(r'"@type":\s*"Recipe"'))
        self.ld = json.loads(ld_tag.text) if ld_tag else None
    
    def get_name(self):
        if(self.ld['name']): return self.ld['name']
        
    def get_steps(self):
        steps = self.ld_get_steps()
        if steps: return steps

    def ld_get_steps(self):
        """Extract how-to steps from `self.ld`."""
        if(not self.ld): return
        
        steps = None
        for key in self.ld:
            value = self.ld[key]
            if(type(value) is not list): continue
            if(type(value[0]) is not dict): continue
            if(value[0]['@type'] != 'HowToStep'): continue
            
            steps = value
        if(not steps): return
            
        return list(step['text'] for step in steps)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    
    with open(args.filename, encoding='utf8') as file:
        html_doc = file.read()
        extractor = HTMLRecipeExtractor(html_doc)
        
        print('Name: ', end='')
        print(extractor.get_name())
        print()
        
        print('Steps:')
        print(extractor.get_steps())
        
        # print('Ingredients:')
        # print(extractor.get_ingredients())
    
   
if __name__ == '__main__':
    main()