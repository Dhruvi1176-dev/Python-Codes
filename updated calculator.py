import streamlit as st
import math

# Page Config
st.set_page_config(page_title="Smart Calculator", page_icon="🖩", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        border-radius: 10px;
        background-color: #262730;
        color: white;
        border: 1px solid #4CAF50;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #4CAF50;
        color: black;
        font-weight: bold;
    }
    .display-box {
        background-color: black;
        color: #00FF00;
        font-size: 28px;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        text-align: right;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🖩 Smart Calculator</h1>", unsafe_allow_html=True)

# Session state for calculator input
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Function to handle button clicks
def press(symbol):
    if symbol == "C":
        st.session_state.expression = ""
    elif symbol == "=":
        try:
            st.session_state.expression = str(eval(st.session_state.expression))
        except:
            st.session_state.expression = "Error"
    else:
        st.session_state.expression += str(symbol)

# Display screen
st.markdown(f"<div class='display-box'>{st.session_state.expression}</div>", unsafe_allow_html=True)

# Calculator button layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
    ["C", "(", ")", "**"]
]

# Render buttons
for row in buttons:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        with cols[i]:
            st.button(btn, on_click=press, args=(btn,))

# Extra scientific operations
st.subheader("Scientific Functions")
sci_cols = st.columns(4)
with sci_cols[0]:
    st.button("√", on_click=press, args=("**0.5",))
with sci_cols[1]:
    st.button("^2", on_click=press, args=("**2",))
with sci_cols[2]:
    st.button("%", on_click=press, args=("%",))
with sci_cols[3]:
    st.button("π", on_click=press, args=(math.pi,))
