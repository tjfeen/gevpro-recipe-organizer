from os import path
from src.Recipe import Recipe
import json
import streamlit as st


class RecipeStorage:
    def __init__(self, filename):
        dirname = path.dirname(__file__)
        self.filepath = path.join(dirname, f'../data/{filename.strip()}.json')

        data = self.read()
        self.recipes = [Recipe(item) for item in data]

    def read(self):
        try:
            with open(self.filepath, 'r+') as file:
                return json.loads(file.read())
        except BaseException:
            return []

    def get_recipes(self):
        return self.recipes

    def save(self):
        """Write the recipe data to file storage."""
        data = json.dumps([r.serialize() for r in self.get_recipes()])
        with open(self.filepath, 'w+') as file:
            file.write(data)

    def add(self, recipe):
        self.recipes.append(recipe)
        self.save()

    def remove(self, recipe):
        self.recipes = [r for r in self.recipes
                        if r.get_id() != recipe.get_id()]
        self.save()
