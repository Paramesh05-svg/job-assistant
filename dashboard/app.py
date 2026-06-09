import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Job Assistant",
    layout="wide"
)

st.title(
    "Cloud & DevOps Job Assistant"
)

excel_file = "data/applied_jobs.xlsx"

if os.path.exists(excel_file):

    df = pd.read_excel(excel_file)

    st.metric(
        "Total Jobs",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.warning(
        "Tracker file not found."
    )
