import streamlit as st
import pandas as pd

st.title("🎈 A Will App")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# File uploader for a single table CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV into a DataFrame
    try:
        df = pd.read_csv(uploaded_file)
        # Display the DataFrame with scrolling if it is large
        st.dataframe(df, use_container_width=True, height=400)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
