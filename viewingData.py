import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("CSV Loader")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    st.write("DataFrame loaded from CSV:")
    st.dataframe(df)

    # Display the first 5 rows of the DataFrame
    st.write("First 5 rows of the DataFrame:")
    st.dataframe(df.head())
    
    # Display some basic information about the DataFrame
    st.write("Basic Information:")
    st.write(df.info())
    
    # Display summary statistics of the DataFrame
    st.write("Summary Statistics:")
    st.write(df.describe())
else:
    st.write("Please upload a CSV file.")
