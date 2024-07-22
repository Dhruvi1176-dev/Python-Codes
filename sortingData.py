import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("Sort DataFrame by Column A")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Check if column units exists in the DataFrame
    if 'Units' in df.columns:
        # Sort the DataFrame by column units in descending order
        sorted_df = df.sort_values(by='Units', ascending=False)
        
        # Display the sorted DataFrame
        st.write("DataFrame sorted by column Units (descending order):")
        st.dataframe(sorted_df)
    else:
        st.write("Column Units is not present in the DataFrame.")
else:
    st.write("Please upload a CSV file.")
