# Spatial project about the movement of people in Sweden based on the learning institutions in that particular area.
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt

# Read in the data. 
file_content = open('Data/institution_data.csv')
file_content_2 = open('Data/Flyttningsöverskott.csv')
file_content_3 = open('Data/Total_befolkning.csv')
file_content_4 = open('Data/Befolkningsförändring.csv')
universities = pd.read_csv(file_content, quotechar='"', delimiter=',')
moving_net = pd.read_csv(file_content_2, quotechar='"', delimiter=',')
population_tot = pd.read_csv(file_content_3, quotechar='"', delimiter=',')
population_change = pd.read_csv(file_content_4, quotechar='"', delimiter=',')

#print(universities)
#print(moving_net)
#print(population_tot)
#print(population_change)

# Make the data frames into lists of integers. 
i = 0
moving_data = []
for column in moving_net:
    if i > 1: # i > 2 to skip 1968 where there is no pop_diff.
        temp = [int(x) for x in list(moving_net[column][2:23])]
        moving_data.append(temp)
    i += 1

# Add both data together to know the total people who moved. 
moving_data = np.reshape(moving_data, (21, 54))

# Remove the region names.
population_tot = population_tot.drop('region', axis = 1)
population_change = population_change.drop('region', axis = 1)

#print(np.shape(moving_data))
#print(np.shape(population_tot))

# Simple regression. 
sweden_tot = population_tot.sum(axis = 0)
years = np.linspace(0, len(sweden_tot) - 1, num=len(sweden_tot)).reshape(-1, 1)
reg = linear_model.LinearRegression().fit(years, sweden_tot) # Change to cooler regression?
# Make predictions using the testing set.
pred = reg.predict(years)
# The coefficients.
print("Coefficients: \n", reg.coef_, reg.intercept_)
# The coefficient of determination.
print("Coefficient of determination: %.2f" % r2_score(sweden_tot, pred))

# Plot outputs
plt.scatter(years, sweden_tot, color="black")
plt.plot(years, pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

# TODO: Find out how I want to do the interpolation. 
# Maybe look at proportion of student population?


# TODO: Add change color based on how many people move in and out. Jikan aru no?

# TODO: Change Sweden map to be the number of students instead!
