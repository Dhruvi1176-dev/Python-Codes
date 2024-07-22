import streamlit as st

# Title of the app
st.title("My Calculator")

# Input fields for the numbers and operation
num1 = st.number_input("Enter the first number")
num2 = st.number_input("Enter the second number")
operation = st.selectbox("Choose an operation", ["Addition", "Subtraction", "Multiplication", "Division"])

# Perform the calculation
if operation == "Addition":
    result = num1 + num2
elif operation == "Subtraction":
    result = num1 - num2
elif operation == "Multiplication":
    result = num1 * num2
elif operation == "Division":
    if num2 != 0:
        result = num1 / num2
    else:
        result = "Error! Division by zero."

# Display the result
st.write("Result:", result)
