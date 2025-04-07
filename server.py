import streamlit as st
import pandas as pd
from src.RecipeStorage import RecipeStorage

storage = RecipeStorage('recipes')
print(storage.read())

st.header('Recipes')

st.dataframe()