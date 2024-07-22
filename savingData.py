import streamlit as st
import pandas as pd
import io

# Title of the Streamlit app
st.title("Save DataFrame to CSV")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Save the DataFrame to a new CSV file named output.csv
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    # Create a download link
    st.download_button(
        label="Download CSV",
        data=output,
        file_name="output.csv",
        mime="text/csv"
    )
    
    # Display the DataFrame
    st.write("DataFrame loaded from CSV:")
    st.dataframe(df)
else:
    st.write("Please upload a CSV file.")
