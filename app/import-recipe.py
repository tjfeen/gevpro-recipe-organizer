from src.Recipe import Recipe
import streamlit as st
import requests
import time

st.set_page_config(page_title='Import recipe', page_icon='🔗')
st.markdown('# Import a recipe 🔗')

url = st.text_input('Enter URL to import the recipe from...', placeholder='https://google.com/...')

if st.button('Import'):
    res = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    
    if res.status_code == 200:
        recipe = Recipe({ 'source': res.text })
        st.session_state['storage'].add(recipe)
        
        st.success(f"Recipe imported succesfully.")
        st.page_link('app/recipes.py')
    else:
        st.error('Failed to extract page content from url.')
