import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import project as ppe # PPE = Placement Probability Estimator

st.set_page_config(page_title='Placement', page_icon='images/mountain_icon.png', layout="centered", initial_sidebar_state="expanded", menu_items=None)

# Title
st.write('''
    # Placement Probabality Estimator
    ### Specific Placement
    ''')

st.sidebar.header('User Input')

folderName = st.sidebar.selectbox(
'Data Source Folder',
["Data"],
index=0
)

# Standing data input
filenameStanding = st.sidebar.file_uploader('Standing Data Source File')

# Rounds left input (Range 1-31)
rounds = st.sidebar.number_input("Number of rounds remaining", value=1, placeholder="Type a number...", min_value = 1, max_value = 31)

# Number of trials in simulation input
numTrials = st.sidebar.number_input("Number of trials", value=100000, placeholder="Type a number...", min_value = 100000, max_value = 500000, step=100000)

toLabel = st.sidebar.selectbox(
'Include Label',
[True, False],
index=0
)

placement = st.sidebar.slider('Placement to Plot (Select from 1 to 16)', 1, 16, None)

# Run Calculation
if placement is not None and filenameStanding is not None:
    teams, standings = ppe.standingRead(filenameStanding) 
    data = ppe.convertToProbResults(ppe.simulation(teams, ppe.compileData(folderName), standings, numTrials, 12), numTrials)
    fig, ax = ppe.visualizeBarPlacement(data, teams, placement, addLabel=toLabel)
    st.pyplot(fig)