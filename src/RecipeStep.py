class RecipeStep:
    def __init__(self, recipe, text):
        self.recipe = recipe
        self.text = text
        
    def get_text(self):
        return self.text