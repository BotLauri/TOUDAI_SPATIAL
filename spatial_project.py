# Spatial project about the movement of people in Sweden based on the learning institutions in that particular area.
import pandas as pd
import numpy as np

# Read in the data. 
file_content = open('Data/institution_data.csv')
file_content_2 = open('Data/Invandringsöverskott.csv')
file_content_3 = open('Data/Flyttningsöverskott.csv')
file_content_4 = open('Data/Total_befolkning.csv')
file_content_5 = open('Data/Befolkningsförändring.csv')
universities = pd.read_csv(file_content, quotechar='"', delimiter=',')
moving_in = pd.read_csv(file_content_2, quotechar='"', delimiter=',')
moving_out = pd.read_csv(file_content_3, quotechar='"', delimiter=',')
population_tot = pd.read_csv(file_content_4, quotechar='"', delimiter=',')
population_change = pd.read_csv(file_content_5, quotechar='"', delimiter=',')

# Make the data frames into lists of integers. 
i = 0
moving_in_data = []
for column in moving_in:
    if i > 1: # i > 2 to skip 1968 where there is no pop_diff.
        temp = [int(x) for x in list(moving_in[column][2:23])]
        moving_in_data.append(temp)
    i += 1
i = 0
moving_out_data = []
for column in moving_out:
    if i > 1:
        temp = [int(x) for x in list(moving_out[column][2:23])]
        moving_out_data.append(temp)
    i += 1

# Add both data together to know the total people who moved. 
moving_data = np.reshape(moving_in_data, (1, 1134)) - np.reshape(moving_out_data, (1, 1134))
moving_data = np.reshape(moving_data, (21, 54))

# Remove the region names.
population_tot = population_tot.drop('region', axis = 1)
population_change = population_change.drop('region', axis = 1)

print(np.shape(moving_data))
print(np.shape(population_tot))


# TODO: Find the average growth per year of population.
# TODO: Find out how I want to do the interpolation. 
# Maybe look at proportion of student population?

# TODO: Clean up. Write a little on the report. 
# TODO: Add change color based on how many people move in and out. 

# TODO: What does each of the columns actually mean? Add to report.
# What is the best one? 
# Probably flyttningsöverskott + Invandringsöverskott.
# Will get dataframes with only those two in the future. 

#Flyttningsöverskott
#Flyttningsöverskott beräknas som skillnaden mellan antal in- och utflyttningar (inrikes och utrikes).
#Invandringsöverskott
#Immigrationsöverskott beräknas som skillnaden mellan antal inflyttade från utlandet (immigranter) och utflyttade till utlandet (emigranter).
#Inrikes inflyttningar
#Med inrikes inflyttningar avses inflyttningar minus immigration.
#Inrikes utflyttningar
#Med inrikes utflyttningar avses utflyttningar minus emigration.

