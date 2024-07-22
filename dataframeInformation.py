import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("DataFrame Summary Information and Statistics")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    st.write("DataFrame loaded from CSV:")
    st.dataframe(df)
    
    # Display summary information about the DataFrame
    st.write("Summary Information:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    # Display summary statistics of the DataFrame
    st.write("Summary Statistics:")
    st.write(df.describe())
else:
    st.write("Please upload a CSV file.")
