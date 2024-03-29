import streamlit as st
import pandas as pd
import numpy as np
from utils import display_data_files, get_score_data
from initial import initial_script, initial_script_without_write

def main():

    
    st.set_page_config(page_title="Book Scanning Optimizer", page_icon=":books:", layout="wide")
    st.title("Book Scanning Optimizer :books:")  
    st.markdown("---")

    initial_script_without_write()
    df = get_score_data()
    st.subheader("Scores")
    df["Best Score"] = df["Initial Score"]
    st.dataframe(df, use_container_width=True)
    
    with st.sidebar:
        st.subheader("Choose the file to run the optimizer")
        st.selectbox("Select file", display_data_files())
        st.button("Run")
        st.write("Results")
        # print(get_results())



if __name__ == "__main__":
    main()