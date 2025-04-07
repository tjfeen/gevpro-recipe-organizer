from os import path
import json

class RecipeStorage:
    def __init__(self, filename):
        dirname = path.dirname(__file__)
        self.filepath = path.join(dirname, f'../data/{filename.strip()}.json')
        
    def read(self):
        try:
            with open(self.filepath, 'r') as file:
                return json.loads(file.read())
        except:
            return []  
        
    def add(self, recipe):
        data = self.read()
        data.append(recipe.serialize())
        
        with open(self.filepath, 'w') as file:
            file.write(json.dumps(data))
        