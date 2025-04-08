import streamlit as st
import json
import os
from src.RecipeStorage import RecipeStorage

if 'storage' not in st.session_state:
    st.session_state['storage'] = RecipeStorage('recipes')

pg = st.navigation([
    st.Page('app/recipes.py', title='📃 View recipes'),
    st.Page('app/import-recipe.py', title='🔗 Import recipe'),
    st.Page('app/write-recipe.py', title='📝 Write recipe')
])

pg.run()

st.write("""
    <style>
        [class*="st-key-flex"] { 
            display: flex; 
            flex-direction: row; 
        }
        
        [class*="st-key-align_right"] { 
            margin-left: auto;
        }
    </style>
""", unsafe_allow_html=True)
