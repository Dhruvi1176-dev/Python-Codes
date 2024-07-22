import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("Add Column C to DataFrame")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Check if columns 'Year' and 'Value' exist in the DataFrame
    if 'Year' in df.columns and 'Value' in df.columns:
        # Convert 'Year' and 'Value' columns to numeric if they are not already
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # coerce will turn non-numeric values to NaN
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        
        # Check if there are NaN values after conversion
        if df[['Year', 'Value']].isnull().values.any():
            st.write("Warning: Non-numeric values found in 'Year' or 'Value' columns.")
        
        # Create a new column 'C' that is the sum of columns 'Year' and 'Value'
        df['C'] = df['Year'] + df['Value']
        
        # Display the updated DataFrame
        st.write("DataFrame with new column C (Year + Value):")
        st.dataframe(df)
    else:
        st.write("Columns 'Year' and/or 'Value' are not present in the DataFrame.")
else:
    st.write("Please upload a CSV file.")
