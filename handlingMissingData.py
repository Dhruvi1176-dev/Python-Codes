import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("Drop Rows with Missing Values")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Drop rows with any missing values
    cleaned_df = df.dropna()
    
    # Display the cleaned DataFrame
    st.write("DataFrame after dropping rows with missing values:")
    st.dataframe(cleaned_df)
else:
    st.write("Please upload a CSV file.")
