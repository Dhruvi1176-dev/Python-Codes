# app.py
import streamlit as st
import requests

st.title("Recipe Search App")

# Your Spoonacular API Key
API_KEY = 'e55076838cca42fcb8213eb8fb3b8377'

# Function to search for recipes
def search_recipes(query):
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}&number=10"
    response = requests.get(url)
    data = response.json()
    return data['results']

# Function to get recipe details
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data

# Search bar
query = st.text_input("Search for recipes")

if query:
    results = search_recipes(query)
    for recipe in results:
        st.write(f"### {recipe['title']}")
        st.image(recipe['image'], width=200)
        if st.button(f"Get details of {recipe['title']}"):
            recipe_details = get_recipe_details(recipe['id'])
            st.write(f"**Title:** {recipe_details['title']}")
            st.write(f"**Servings:** {recipe_details['servings']}")
            st.write(f"**Ready in:** {recipe_details['readyInMinutes']} minutes")
            st.write(f"**Instructions:** {recipe_details['instructions']}")
            st.image(recipe_details['image'], width=400)
