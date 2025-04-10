# Recipe Organizer

We developed a system that allows users to extract recipes directly from a provided URL. The extracted recipe is displayed in a user-friendly interface, where users can also manually add and remove their own recipes. Each recipe includes detailed instructions and supports a personal rating system.

---

## Contributors

This project was made by **Liam**, **Tjalling**, and **Tobiasz**.

- **Tjalling** developed the Python-based extraction system that can extract a full recipe from provided links and added sample data.
- **Liam** and **Tobiasz** worked on making the interface functional and visually appealing.
- **Tobiasz** also ensured that all files follow the correct code style using pycodestyle.
- **Liam** additionally wrote test cases to verify that adding, saving, and removing recipes works correctly.

---

## Instructions on Usage

### Installation

1. Clone the GitHub repository to your device and open it in any code editor (for instance, Visual Studio Code).

2. Install the required dependencies using 'pip install -r requirements.txt`

### Running

1. Launch web server using `streamlit run app.py` (or `python3 -m streamlit run app.py`)

2. This should open https://localhost:8501

3. From here: 
- Paste a recipe link to extract a full recipe automatically
- Or manually add your own recipes using the input form 
- Recipes will be saved and displayed in the "View Recipes" tab 
- All recipe data is stored in recipes.json 