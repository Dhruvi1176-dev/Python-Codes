import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("CSV Column Selector")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Check if columns A and B exist in the DataFrame
    if 'Industry_code_NZSIOC' in df.columns and 'Units' in df.columns:
        # Select columns A and B
        selected_columns = df[['Industry_code_NZSIOC', 'Units']]
        
        # Display the selected columns 
        st.write("Selected Columns (A and B):")
        st.dataframe(selected_columns)
    else:
        st.write("Columns A and/or B are not present in the DataFrame.")
else:
    st.write("Please upload a CSV file.")
