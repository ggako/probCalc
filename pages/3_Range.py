import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import project as ppe # PPE = Placement Probability Estimator

st.set_page_config(page_title='Placement', page_icon='images/mountain_icon.png', layout="centered", initial_sidebar_state="expanded", menu_items=None)

# Title
st.write('''
    # Placement Probabality Estimator
    ### Range Placement (Specified Range) (e.g. Top 8, Bottom 8, Between 3-5)
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

# Upper placement
upper = st.sidebar.number_input("Insert upper placement (1 to 15)", value=None, placeholder="", min_value = 1, max_value = 15)

# Lower placement
lower = st.sidebar.number_input("Insert lower placement (2 to 16)", value=None, placeholder="", min_value = 2, max_value = 16)

# Run Calculation
if upper is not None and lower is not None and filenameStanding is not None:
    teams, standings = ppe.standingRead(filenameStanding) 
    data = ppe.convertToProbResults(ppe.simulation(teams, ppe.compileData(folderName), standings, numTrials, rounds), numTrials)
    fig, ax = ppe.visualizeProbRangeResults(ppe.probRangeResults(data, upper, lower), teams, upper, lower, addLabel=True, color_base="mediumslateblue")
    st.pyplot(fig)