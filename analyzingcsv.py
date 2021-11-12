import pandas as pd
from datetime import datetime

data = pd.read_csv("survey 2.csv")

#melting dataset to get only the columns I want
columns = ['Timestamp', 'Age', 'Gender', 'Country', 'state', 'work_interfere', 'benefits', 'leave', 'supervisor', 'tech_company']
data = data[columns]

#now I want to transform timestamp column to only show the date for simplicity
data["Timestamp"] = pd.to_datetime(data["Timestamp"]).dt.date #using pandas to_datetime function
#now to change the column name to date instead of timestamp
data.rename(columns={"Timestamp": "Date"}, inplace=True)

#fixing gender values (keeping data consistent. assigning other to those who don't identify as male or female.)
maleFix = ['M', 'm', 'male', 'man']
femaleFix = ['F', 'f', 'female', 'Woman']
otherList = []
data["Gender"] = data["Gender"].replace(dict.fromkeys(maleFix, 'Male'))
data["Gender"] = data["Gender"].replace(dict.fromkeys(femaleFix, 'Female'))
for i in data["Gender"]:
    if i != "Male" and i != "Female":
        otherList.append(i)
data["Gender"] = data["Gender"].replace(dict.fromkeys(otherList, "Other"))



#saving file to new csv
data.to_csv("newsurvey.csv", sep=',', index=False)

for col in data:
    print(col)







