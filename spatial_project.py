# Spatial project about the movement of people in Sweden based on the learning institutions in that particular area.
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt

# Read in the data. 
file_content = open('Data/institution_data.csv')
file_content_2 = open('Data/Inflyttningar.csv')
file_content_3 = open('Data/Invandringar.csv')
file_content_4 = open('Data/Total_befolkning.csv')
file_content_5 = open('Data/Befolkningsförändring.csv')
universities = pd.read_csv(file_content, quotechar='"', delimiter=',')
moving_in = pd.read_csv(file_content_2, quotechar='"', delimiter=',')
immigration = pd.read_csv(file_content_3, quotechar='"', delimiter=',')
population_tot = pd.read_csv(file_content_4, quotechar='"', delimiter=',')
population_change = pd.read_csv(file_content_5, quotechar='"', delimiter=',')

#print(universities)
#print(moving_in)
#print(immigration)
#print(population_tot)
#print(population_change)

# Make the data frames into lists of integers. 
i = 0
moving_in_data = []
for column in moving_in:
    if i > 0: # Remove first column.
        temp = [int(x) for x in list(moving_in[column][:])]
        moving_in_data.append(temp)
    i += 1

i = 0
immigration_data = []
for column in immigration:
    if i > 0:
        temp = [int(x) for x in list(immigration[column][:])]
        immigration_data.append(temp)
    i += 1

moving_data = np.reshape(moving_in_data, (1, 1134)) + np.reshape(immigration_data, (1, 1134))

# Add both data together to know the total people who moved. 
moving_data = np.reshape(moving_data, (54, 21)) # 54 years and 21 different counties. 
moving_data = np.transpose(moving_data)

# Remove the region names.
population_tot = population_tot.drop('region', axis = 1)
population_change = population_change.drop('region', axis = 1)
population_change = population_change.drop('Folkökning 1968', axis = 1)

#print(np.shape(moving_data))
#print(np.shape(population_tot))

# Simple regression. 
sweden_tot = population_tot.sum(axis = 0)
sweden_change = population_change.sum(axis = 0)
years = np.linspace(0, len(sweden_tot) - 1, num=len(sweden_tot)).reshape(-1, 1)
years2 = np.linspace(0, len(sweden_tot) - 1, num=len(sweden_change)).reshape(-1, 1)
reg = linear_model.LinearRegression().fit(years, sweden_tot)
reg2 = linear_model.LinearRegression().fit(years2, sweden_change)
# Make predictions using the testing set.
pred_tot = reg.predict(years)
pred_change = reg2.predict(years2)
#print("Coefficients: \n", reg.coef_, reg.intercept_)
# The coefficient of determination.
#print("Coefficient of determination: %.2f" % r2_score(sweden_tot, pred_tot))

# Plot outputs
#plt.scatter(years, sweden_tot, color="black", label='Population data')
#plt.plot(years, pred_tot, color="blue", linewidth=2, label='Linear regression')
#plt.title('Swedens population and a linear regression.')
#plt.legend()
#plt.xticks(())
#plt.yticks(())
#plt.show()

# Get proportion pop which is just a proportion of tot_pop. 
# Sum each county. 
pop_county_tot = population_tot.sum(axis = 1)
# Sum to get total popluation. 
pop_tot = pop_county_tot.sum(axis = 0)
# Get proportions and assume everything is linear. 
pop_tot_proportion = pop_county_tot / pop_tot
pop = []
for i in range(len(pop_tot_proportion)):
    temp = [x*pop_tot_proportion[i] for x in pred_tot]
    pop.append(temp)

#print(np.shape(pop))

# Get enrolled_student_proportion. 
number_of_enrolled = np.zeros(21)
for i in range(len(universities)):
    county = int(universities['county'][i])
    if county >= 17:
        county -= 5
    elif county >= 12:
        county -= 3
    elif county >= 3:
        county -= 2
    else:
        county -= 1
    temp = int(universities['Number of new entrants'][i])
    number_of_enrolled[county] += temp
    
population_county_2018 = list(population_tot[:]['Folkmängd 2018'])
enrolled_student_proportion = np.divide(number_of_enrolled, population_county_2018)

#print(number_of_enrolled)
#print(list(population_tot[:]['Folkmängd 2018']))
#print(enrolled_student_proportion)

# Prepare the population data for regression. 
data = []
for column in population_tot:
    if i > 0:
        temp = [int(x) for x in list(population_tot[column][:])]
        data.append(temp)
    i += 1
data = np.transpose(data)

data2 = []
for column in population_change:
    if i > 0:
        temp = [int(x) for x in list(population_change[column][:])]
        data2.append(temp)
    i += 1
data2 = np.transpose(data2)

# Do the regressions. 
betas = np.zeros(len(data))
R2s = np.zeros(len(data))
OGR2s = np.zeros(len(data))

for i in range(len(data)):
    # fit_intercept False makes the data centered, which we want. (We do not want a constant factor.)
    reg = linear_model.LinearRegression(fit_intercept = False).fit(years, (data[i][:] - pop[i][:])*enrolled_student_proportion[i])
    betas[i] = reg.coef_[0]
    pred = reg.predict(years)
    R2s[i] = r2_score((data[i][:] - pop[i][:])*enrolled_student_proportion[i], pred)
    OGR2s[i] = r2_score(data2[i][:], pred_change*pop_tot_proportion[i])

print(betas)
print(R2s)
#print(OGR2s)
