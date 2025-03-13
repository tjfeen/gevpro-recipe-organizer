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
        search_query = st.text_input("Search for a savrecipe")
        filtered_recipes = {k: v for k, v in st.session_state["recipes"].items() if search_query.lower() in k.lower()}
        
        for recipe, data in list(filtered_recipes.items()):  # Use list() to allow removal
            st.subheader(recipe)
            st.write(f"**Ingredients:**\n{data['ingredients']}")
            st.write(f"**Instructions:**\n{data['instructions']}")

            # Inject CSS and JavaScript for star rating
            star_html = """
            <style>
                .star-container {
                    display: flex;
                    gap: 5px;
                }
                .star {
                    font-size: 30px;
                    cursor: pointer;
                    color: #888;  /* Default gray */
                    text-shadow: 0px 0px 4px rgba(255, 255, 255, 0.5); /* Soft glow */
                    transition: color 0.2s ease-in-out, text-shadow 0.2s ease-in-out;
                }
                .selected {
                    color: gold;
                    text-shadow: 0px 0px 8px rgba(255, 215, 0, 0.8); /* Gold glow */
                }
            </style>
            <script>
                function selectStars(recipe, value) {
                    fetch('/?recipe=' + recipe + '&rating=' + value, {method: 'POST'});
                    localStorage.setItem(recipe + '_rating', value);
                    for (let i = 1; i <= 5; i++) {
                        let star = document.getElementById(recipe + '_star_' + i);
                        star.className = (i <= value) ? 'star selected' : 'star';
                    }
                }
                document.addEventListener("DOMContentLoaded", function() {
                    document.querySelectorAll(".star-container").forEach(container => {
                        let recipe = container.getAttribute("data-recipe");
                        let savedRating = localStorage.getItem(recipe + '_rating');
                        if (savedRating) {
                            for (let i = 1; i <= 5; i++) {
                                let star = document.getElementById(recipe + '_star_' + i);
                                star.className = (i <= savedRating) ? 'star selected' : 'star';
                            }
                        }
                    });
                });
            </script>
            """

            rating = st.session_state["recipes"].get(recipe, {}).get("rating", 0)
            stars = f'<div class="star-container" data-recipe="{recipe}">' + "".join(
                f'<span id="{recipe}_star_{i}" class="star {"selected" if i <= rating else ""}" onclick="selectStars(\'{recipe}\', {i})">&#9733;</span>'
                for i in range(1, 6)
            ) + '</div>'

            st.components.v1.html(star_html + stars, height=50)

            note = st.text_area(f"Notes for {recipe}", value=data["note"])

            # Buttons in a row with minimal spacing
            col1, col2 = st.columns([1, 1])  # Evenly distributed columns
            with col1:
                if st.button(f"Save {recipe}", key=f"save_{recipe}"):
                    st.session_state["recipes"][recipe]["note"] = note
                    st.session_state["recipes"][recipe]["rating"] = rating
                    save_recipes(st.session_state["recipes"])
                    st.success(f"Saved '{recipe}'!")

            with col2:
                if st.button(f"Remove {recipe}", key=f"remove_{recipe}"):
                    del st.session_state["recipes"][recipe]
                    save_recipes(st.session_state["recipes"])