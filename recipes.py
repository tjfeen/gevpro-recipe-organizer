import streamlit as st
import json
import os

st.set_page_config(page_title="Recipe Organizer", page_icon="🍽", layout="wide")

DATA_FILE = "recipes.json"

# Function to load recipes from file
def load_recipes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Function to save recipes to file
def save_recipes(recipes):
    with open(DATA_FILE, "w") as f:
        json.dump(recipes, f, indent=4)

# Load recipes into session state
if "recipes" not in st.session_state:
    st.session_state["recipes"] = load_recipes()

# Sidebar Navigation Menu
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Select Page", ["Add Recipe", "Saved Recipes"])

if page == "Add Recipe":
    st.markdown("# Add a New Recipe")

    recipe_name = st.text_input("Recipe Name")
    ingredients = st.text_area("Ingredients")
    instructions = st.text_area("Instructions")

    if st.button("Save Recipe"):
        if recipe_name:
            st.session_state["recipes"][recipe_name] = {
                "ingredients": ingredients,
                "instructions": instructions,
                "rating": 0,  # Default rating
                "note": ""
            }
            save_recipes(st.session_state["recipes"])  # Save to file
            st.success(f"Recipe '{recipe_name}' saved!")
        else:
            st.warning("Please enter a recipe name.")

elif page == "Saved Recipes":
    st.markdown("# Saved Recipes")

    if not st.session_state["recipes"]:
        st.write("No recipes saved yet.")
    else:
        search_query = st.text_input("Search for a recipe")
        filtered_recipes = {k: v for k, v in st.session_state["recipes"].items() if search_query.lower() in k.lower()}

        if not filtered_recipes:
            st.write("No recipes found for your search.")

        for recipe, data in filtered_recipes.items():
            st.subheader(recipe)
            st.write(f"**Ingredients:**\n{data['ingredients']}")
            st.write(f"**Instructions:**\n{data['instructions']}")

            # Display the current rating with radio buttons (1 to 5 stars), but allow 0 as well
            rating = st.session_state["recipes"].get(recipe, {}).get("rating", 0)
            rating_options = ["No Rating", "1 star", "2 stars", "3 stars", "4 stars", "5 stars"]

            # Radio buttons for selecting the rating (horizontal display)
            new_rating = st.radio(f"Rate {recipe}", options=rating_options, index=rating, key=f"rating_{recipe}", horizontal=True)

            # Adjust new_rating to reflect the correct index (1-based for stars)
            if new_rating != "No Rating":
                new_rating_value = rating_options.index(new_rating)
            else:
                new_rating_value = 0

            # Update rating if it's changed
            if new_rating_value != rating:
                st.session_state["recipes"][recipe]["rating"] = new_rating_value
                save_recipes(st.session_state["recipes"])  # Save updated rating to recipes.json
                st.success(f"Rating for '{recipe}' updated to {new_rating_value} stars!" if new_rating_value > 0 else f"Rating for '{recipe}' removed!")

            # Display and update notes
            note = st.text_area(f"Notes for {recipe}", value=data["note"])

            # Buttons in a row
            col1, col2 = st.columns(2)  # Create two columns for the buttons to be placed horizontally
            with col1:
                if st.button(f"Save {recipe}", key=f"save_{recipe}"):
                    st.session_state["recipes"][recipe]["note"] = note
                    save_recipes(st.session_state["recipes"])
                    st.success(f"Saved notes for '{recipe}'!")

            with col2:
                if st.button(f"Remove {recipe}", key=f"remove_{recipe}"):
                    del st.session_state["recipes"][recipe]
                    save_recipes(st.session_state["recipes"])
                    st.success(f"Removed '{recipe}'!")
