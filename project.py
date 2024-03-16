import numpy as np
import pandas as pd
import csv
import os
import random
import matplotlib.pyplot as plt


def visualizeResultsHeatmap(results, teams, threshold = None, colorlimit = 25, saveShow = True):
    """
    Returns a heatmap of results

    Reference: https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html

    Note: 
    threshold - Below threshold, the cell will not be annotated
    colorlimit - Below color limit annotations will be black, above will be white for readability
    saveShow - saves and show figure - use False when calling from application
    """

    # fig, ax = plt.subplots()
    # im = ax.imshow(results)

    # Heat map
    fig, ax = plt.subplots(figsize=(12,12))
    # ax.imshow(results, cmap='OrRd')
    # ax.imshow(results, cmap='YlGn')
    ax.imshow(results, cmap='winter')

    # Making x-label
    placements = [x + 1 for x in range(len(teams))]

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(placements)), labels=placements)
    ax.set_yticks(np.arange(len(teams)), labels=teams)
    ax.tick_params(top=True, labeltop=True, bottom=True, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    # Case: no threshold indicated - adds annotation to all cells
    if threshold == None:
        for i in range(len(teams)):
            for j in range(len(placements)):
                text = ax.text(j, i, round(results[i, j],2),
                            ha="center", va="center", color="k")    
    # Case: threshold indicated - only adds annotation to cells above the threshold
    else:
        for i in range(len(teams)):
            for j in range(len(placements)):
                if results[i, j] >= threshold:
                    if results[i, j] < colorlimit:
                        text = ax.text(j, i, round(results[i, j],2),
                                    ha="center", va="center", color="w")  
                    else:
                        text = ax.text(j, i, round(results[i, j],2),
                                    ha="center", va="center", color="k")  
                else:
                    pass  
            
    ax.set_title("Tournament Placement Heatmap")
    fig.tight_layout()

    if saveShow == True:
        plt.savefig('probability.png')
        plt.show()

    return fig, ax


def standingRead(filename):
    """
    Input: filename of standing

    Reads teams and current standing data

    Returns two list (team and standing)
    """

    # Read as numpy array, transpose then convert to list
    data = np.loadtxt(filename, delimiter=",", dtype=str).transpose().tolist()

    teams = data[0]
    standings = [int(x) for x in data[1]]
        
    return teams, standings


def averagePPG(data):
    """
    Returns a dataframe of points per game
    """

    placement = [int(x) for x in range(1,17)]

    averagePPG = []
    totalRounds = len(data[0]) # Note: data has 16 lists representing each placement with length: total number of rounds

    # Computing averages
    for dataRow in data:

        average = sum(dataRow) / totalRounds

        averagePPG.append(average)

    # Creating dataframe
    ppg_dict = {'Placement': placement , 'PPG': averagePPG}
    ppg_df = pd.DataFrame(ppg_dict).set_index('Placement').round({'PPG':2})

    return ppg_df


def simulation(teams, data, standings, numTrials, roundsLeft):
    """
    Output: probability of each team getting 1,2,3,4,5,6....16th place

    Returns: 

    numpy array of results in win count format
    # Rows represent team, columns represent placement
    """

    # Note results contains the information of how many times a team got / tally of a certain placement during simulation
    results = np.zeros((len(teams), len(teams)), dtype=int) 
    placements = list(range(len(teams)))
    totalGames = np.shape(data)[1]

    # Simulate tournaments
    for _ in range(numTrials):

        # Make copy of current standings
        standingsCopy = standings.copy()

        # Simulate games
        for _ in range(roundsLeft):

            # Select random game - will be selected via index
            gameIndex = random.randint(0, totalGames - 1)
            gamePoints = data[:,gameIndex]

            # Shuffle placements (Teams will be assigned a random placement based from this list)
            np.random.shuffle(placements)

            # Add points to current standing
            for k in range(16):
                standingsCopy[k] += gamePoints[placements[k]]

        # Get tournament placement
        tournPlacement = getTournPlacement(standingsCopy)
        # Decrement by 1 since lowest value starts with 1, need to start with 0 for accessing using index
        tournPlacement = [x - 1 for x in tournPlacement] 

        # Add placements to result 
        for k in range(16):
            results[k][tournPlacement[k]] += 1

    # print(standingsCopy)
    # print(tournPlacement)
    # print(results)

    return results


def convertToProbResults(results, numTrials):
    """
    Returns probability equivalent of results (which is in tally format)
    """

    # Convert results in probability format - simply divide whole array by numTrials
    probResults = np.copy(results)
    probResults = np.divide(probResults, numTrials/100)
    np.set_printoptions(suppress=True) # To suppress printing with default scientific notation

    # print(probResults)

    return probResults


def getTournPlacement(input):
    """
    Returns placement from a given list (1 corresponds to largest item in output)

    e.g. input = [1, 2, 3, 4, 0] ---> output = [4, 3, 2, 1, 5]

    https://codereview.stackexchange.com/questions/65031/creating-a-list-containing-the-rank-of-the-elements-in-the-original-list
    by mjolka
    """

    indices = list(range(len(input)))
    indices.sort(key=lambda x: input[x])
    output = [0] * len(indices)
    for i, x in enumerate(indices):
        # output[x] = i  
        output[x] = len(input) - i  # Modified to len(input) - i to reverse order, 1 is the largest

    return output  


def compileData(folderName):
    """
    Combines all data from all files in folder - including subfolders
    Assumes csv file is in correct readable format
    Note: Calls readData function

    Returns numpy array of shape (16, number of rounds from all files)
    """

    # Initialize file name list
    filelist = []

    # Get all csv files in folder
    for root, dirs, files in os.walk(folderName):
        for file in files:
            #append the file name to the list
            if(file.endswith(".csv")):
                filelist.append(os.path.join(root,file))

    # Check if file is empty
    if len(filelist) == 0:
        raise Exception("No csv files found")

    # Initialize data
    dataExist = False # Used for initialization

    # Fill data variable
    for name in filelist:
        # Initialization case
        if dataExist == False:
            data = readData(name)
            dataExist = True
        # Concatenate data column wise
        else:
            data = np.concatenate((data, readData(name)), axis=1)

    return data


def readData(filename):
    """
    Reads csv file

    Returns numpy array of shape (16, number of rounds)
    """

    with open(filename) as file:

        csvreader = csv.reader(file, delimiter=",")

        # Placeholder: list of list of rows (for reading)
        rows = []

        for row in csvreader:

            row = [int(x) for x in row]
            rows.append(row)

        rowsize = len(rows[0]) # rowsize = number of games * 2 (1 column for kills and placement)

        # Converts from placement and kills per round to total points per round (new row size = number of rounds)
        game_rows = []

        # Create each row of game_rows
        for row in rows:

            game_row = []

            for index in range(rowsize):

                # Placements: Even index - Start: 0 - End: Rowsize - 2
                # Add placement points
                if index % 2 == 0:
                    # Create game with no points
                    points = 0
                    if int(row[index]) == 1:
                        points += 10
                    elif int(row[index]) == 2:
                        points += 6
                    elif int(row[index]) == 3:
                        points += 5
                    elif int(row[index]) == 4:
                        points += 4
                    elif int(row[index]) == 5:
                        points += 3
                    elif int(row[index]) == 6:
                        points += 2
                    elif int(row[index]) == 7 or int(row[index]) == 8:
                        points += 1
                    else:
                        pass

                # Kills: Odd index- Start: 1 - End: Rowsize - 1
                # Add kill points
                else:
                    points += int(row[index])

                    # Append points to game_row
                    game_row.append(points)
            
            game_rows.append(game_row)

    # Convert data to numpy array 
    data = np.array(game_rows)

    return data


def main():

    # print(readData('Data/EU/EU_ProtalityS8_GrandFinals.csv'))
    # print(compileData('EmptyFolder')) # Should raise exception
    # print(compileData('Data'))
    # print(np.shape(compileData('Data'))) 
    # print(averagePPG(compileData('Data')))
    # teams, standings = standingRead('PTC_Phase1_Standing.csv')
    # print(teams)
    # print(standings)
    teams, standings = standingRead('PCR2024_Season1_Standing.csv') 
    numTrials = 100000
    data2 = convertToProbResults(simulation(teams, compileData('Data'), standings, numTrials, 12), numTrials)
    visualizeResultsHeatmap(data2, teams, 0.8, 25)
    # print(data2)


if __name__ == "__main__":
    main()