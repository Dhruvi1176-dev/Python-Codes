import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("CSV Filter")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Check if column A exists in the DataFrame
    if 'Year' in df.columns:
        # Filter the DataFrame where column A's value is greater than 50
        filtered_df = df[df['Year'] > 50]
        
        # Display the filtered DataFrame
        st.write("Filtered DataFrame (rows where Year > 50):")
        st.dataframe(filtered_df)
    else:
        st.write("Column A is not present in the DataFrame.")
else:
    st.write("Please upload a CSV file.")

