# Spatial project about the movement of people in Sweden 
# based on the learning institutions in that particular area.

# Set up. 
setwd("~/GitHub/TOUDAI_SPATIAL")
df <- read.csv(file = "data_kommuner.csv", header=FALSE, stringsAsFactors=FALSE, fileEncoding="latin1")
df2 <- read.csv(file = "data_län_ålder.csv", header=FALSE, stringsAsFactors=FALSE, fileEncoding="latin1")
# TODO: Fix the institution data and get the decreases data frames.
# TODO: Get both data before 96 and after 96 and merge them to get data of the whole system. 

# TODO: Add change color based on how many people move in and out. 
# 
# TODO: What does each of the columns actually mean? 
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

print(df[1:2, 3:263]) # All data.
