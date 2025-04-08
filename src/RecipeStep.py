class RecipeStep:
    def __init__(self, recipe, text):
        self.recipe = recipe
        self.text = text

    def get_text(self):
        """Get the display text for this how-to step."""
        return self.text
