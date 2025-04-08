import re

HTML_DOC_PATTERN = re.compile(r'<\s*html.*html\s*/>', re.I)


class RecipeExtractor:
    def __init__(self, recipe, override_source=None):
        self.recipe = recipe
        self.override_source = override_source

        self._load()

    def _load(self):
        """Load the recipe."""
        pass

    def get_source(self):
        """Get the source that the extractor should work with."""
        if (self.override_source):
            return self.override_source
        return self.recipe.get_source()

    @staticmethod
    def accepts(recipe):
        """Check if the extractor can parse the given recipe."""
        return False

    def get_title(self):
        """Get the title for `self.recipe`."""
        pass

    def get_ingredients(self):
        """Get the ingredients needed for `self.recipe`."""
        pass

    def get_steps(self):
        """Get the how-to steps for `self.recipe`."""
        pass
