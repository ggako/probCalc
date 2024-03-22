import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import project as ppe # PPE = Placement Probability Estimator

st.set_page_config(page_title='PPG Recommender', page_icon='images/mountain_icon.png', layout="centered", initial_sidebar_state="expanded", menu_items=None)

# Title
st.write('''
    # Placement Probabality Estimator
    ### PPG Recommender
    ''')

folderName = st.sidebar.selectbox(
'Data Source Folder',
["Data"],
index=0
)

# Standing data input
filenameStanding = st.sidebar.file_uploader('Standing Data Source File')

# Rounds completed (Range 1-31)
roundsCompleted = st.sidebar.number_input("Number of rounds completed", value=1, placeholder="Type a number...", min_value = 1, max_value = 31)

# Rounds left input (Range 1-31)
roundsLeft = st.sidebar.number_input("Number of rounds remaining", value=1, placeholder="Type a number...", min_value = 1, max_value = 31)

# Run Calculation
if st.sidebar.button('Recommend') and filenameStanding is not None: 

    teams, standings = ppe.standingRead(filenameStanding) 
    targetPpgMax, targetPpgAve, targetPpgMin = ppe.ppgRecoMatrix(standings, teams, folderName , roundsCompleted, roundsLeft)
    st.caption('Below are the maximum, average and minimum recommended PPG (points per game) to achieve different placements. Note: The highest placement with a 0 value could be interpreted as the lowest probable placement a team can drop to.')
    st.caption('Values does not imply achieving the recommendation will lead to the placement. Rather, it should be only be used as a guide for setting targets.')
    st.caption('Evaluating PPG of other teams and feasibility of PPG recommendation should be considered during interpretation.')
    st.header('Max Recommended PPG', divider='violet')
    st.dataframe(targetPpgMax)
    st.header('Average Recommended PPG', divider='violet')
    st.dataframe(targetPpgAve)
    st.header('Min Recommended PPG', divider='violet')
    st.dataframe(targetPpgMin)