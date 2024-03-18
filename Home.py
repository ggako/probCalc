import streamlit as st

st.set_page_config(page_title='Placement Probabality Estimator', page_icon='images/mountain_icon.png', layout="centered", initial_sidebar_state="expanded", menu_items=None)

st.write("# Placement Probabality Estimator")

st.markdown(
    """
    This application is built to visualize the estimated probabilities reaching a certain placement in a tournament of teams which is calculated using simulation.
    There are currently two available visualizations which can be selected at the sidebar:
    - **Heatmap**: to see the overall scope of probability distributions
    - **Placement**: to see only the distribution for a specific placement
"""
)
