from src.Recipe import Recipe
import streamlit as st

st.set_page_config(page_title='Write recipe', page_icon='📝')
st.markdown('# Write a recipe 📝')

source = {}
source['title'] = st.text_input('Title', placeholder='Your delicious recipe')
source['ingredients'] = st.text_area(
    'Ingredients', placeholder='The ingredients you need...'
                               '(Use enter to seperate each ingredient)...')
source['steps'] = st.text_area(
    'Steps', placeholder='The steps to make this delicious food '
                         '(Use enter to seperate each step)...')
source['yield'] = st.number_input('How many people does this recipe serve?',
                                  value=4)

if st.button('Save'):
    if not source['title']:
        st.warning('Please enter a recipe name.')
        pass

    recipe = Recipe({'source': source})
    st.session_state['storage'].add(recipe)

    st.success(f"Recipe saved succesfully.")
    st.page_link('app/recipes.py')
