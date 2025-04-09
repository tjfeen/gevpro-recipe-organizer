import streamlit as st
from src.RecipeStorage import RecipeStorage


@st.dialog('Change rating ⭐', width='large')
def rate(recipe):
    # Radio buttons for selecting the rating (horizontal display)
    rating_options = ['No Rating', '1 star', '2 stars',
                      '3 stars', '4 stars', '5 stars']
    rating_input = st.radio('Rate this recipe to change ' +
                            'the order in which it appears.',
                            options=rating_options,
                            index=recipe.get_rating(),
                            key=f'rating_{recipe}',
                            horizontal=True)
    new_rating = rating_options.index(rating_input)

    if new_rating != recipe.get_rating():
        recipe.set_rating(new_rating)
        st.session_state['storage'].save()
        st.rerun()


@st.dialog('Delete recipe 🗑️')
def delete(recipe):
    st.write(f"Do you really want to delete *{recipe.get_title()}*?")

    if st.button('Yes, delete 🗑️'):
        st.session_state['storage'].remove(recipe)
        st.rerun()


st.set_page_config(page_title='View recipes', page_icon='📃')

recipe_yield = None
with st.container(key='flex_1'):
    st.markdown('# Recipes 📃')
    recipe_yield = st.number_input('How many people would you like to serve?',
                                   key='align_right_1',
                                   value=4,
                                   min_value=1,
                                   step=1)

recipes = st.session_state['storage'].get_recipes()

if not len(recipes):
    st.write('No recipes saved yet.')
else:
    # Sort recipes by rating
    sorted_recipes = sorted(recipes,
                            key=lambda r: r.get_rating(), reverse=True)
    for recipe in sorted_recipes:
        title = recipe.get_title() + ' ' + '⭐' * recipe.get_rating()

        with st.expander(title):

            with st.container(key=f'flex_2_{recipe}'):
                rate_button = st.button('Change rating ⭐',
                                        key=f'rate_{recipe}')
                delete_button = st.button('Delete 🗑️',
                                          key=f'delete_{recipe}')

            if rate_button:
                rate(recipe)

            if delete_button:
                delete(recipe)

            st.write('#### Ingredients 🍎')

            if (len(recipe.get_ingredients())):
                for ingredient in recipe.get_ingredients():
                    st.write('- ' + ingredient.get_text(recipe_yield))
            else:
                st.write('No ingredients available.')

            st.write('#### Steps 🥣')
            if (len(recipe.get_steps())):
                for i, step in enumerate(recipe.get_steps()):
                    st.write(f'{i + 1}. {step.get_text()}')
            else:
                st.write('No how-to steps available.')
