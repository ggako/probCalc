import streamlit as st

st.set_page_config(page_title='Placement Probabality Estimator', page_icon='images/mountain_icon.png', layout="centered", initial_sidebar_state="expanded", menu_items=None)

st.write("# Placement Probabality Estimator")

st.markdown(
    """
    This application is built to visualize the estimated probabilities reaching a certain placement in a tournament of teams which is calculated using simulation.
    There are currently three available visualizations which can be selected at the sidebar:
    - **Heatmap**: to see the overall landscape of probability distributions
    - **Placement**: to see the distribution for a specific placement
    - **Range**: to see the distribution for a specific range of placement (e.g. % Chance of getting Top 4, Bottom 8, Rank 6-10)
    - **Floor Expected Ceiling**: to see the floor, expected range, ceiling of placements of teams after the tournament
    - **PPG Recommender**: to see the recommended PPG for the remaining rounds to achieve a certain placement by the end of the tournament
    """
)
