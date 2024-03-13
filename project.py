import numpy as np
import csv

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

    print(readData('Data/EU_ProtalityS8_GrandFinals.csv'))


if __name__ == "__main__":
    main()