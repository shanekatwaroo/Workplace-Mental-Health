import mysql.connector
import csv
from tabulate import tabulate

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="MentalHealth"
)
mycursor = db.cursor(buffered=True)

mycursor.execute('DROP TABLE IF EXISTS survey')
sql = """CREATE TABLE survey (
            Date DATE,
            Age INT(64),
            Gender varchar(10),
            Country varchar(50),
            state varchar(50),
            work_interfere varchar(50),
            benefits varchar(50),
            medLeave varchar(50),
            supervisor varchar(50),
            tech_company varchar(50));"""  # adds columns to table
mycursor.execute(sql)

# now we input values into these columns
data = open('newsurvey.csv')
csv = csv.reader(data, delimiter=',')
all_values = []
next(csv)
for row in csv:
    flag = True
    if len(row[1]) > 4:
        flag = False
    if flag == True:
        value = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        all_values.append(value)

sqlinsert = "INSERT INTO survey VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
mycursor.executemany(sqlinsert, all_values)
db.commit()
# db.commit() when making changes to table, db.commit()
# now we have all the data into the database

# KPI 1: Feelings that mental health affects workplace activity based on gender.
query = """SELECT Gender, 
COUNT(CASE WHEN work_interfere = "Often" THEN 1 END) AS Often, 
COUNT(CASE WHEN work_interfere = "Rarely" THEN 2 END) AS Rarely,
COUNT(CASE WHEN work_interfere = "Never" THEN 3 END) AS Never, 
COUNT(CASE WHEN work_interfere = "Sometimes" THEN 4 END) AS Sometimes, 
COUNT(Gender) AS Total
FROM survey
GROUP BY Gender
"""
mycursor.execute(query)
result = mycursor.fetchall()
#print('"Mental Health affects workplace activities"')
#print(tabulate(result, headers=["Gender","Often","Rarely","Never","Sometimes","Total"], tablefmt="pretty"))

#KPI 2 Age distribution in which mental health affects workplace activities
query2 = """
SELECT Age, COUNT(work_interfere)
FROM survey
WHERE work_interfere = "Often" or work_interfere = "Sometimes"
GROUP BY Age
ORDER BY COUNT(work_interfere) desc LIMIT 5;
"""
mycursor.execute(query2)
result = mycursor.fetchall()
print('"Feelings that mental health affects workplace activities based on age"')
print(tabulate(result, headers=["Age","Count"], tablefmt="pretty"))

#KPI 3: Which states provides the most mental health benefits to employees?
query3 = """
SELECT state, COUNT(benefits)
FROM survey
WHERE benefits = "Yes" and Country IN("United States")
GROUP BY state
ORDER BY COUNT(benefits) DESC LIMIT 5;
"""
mycursor.execute(query3)
result = mycursor.fetchall()
print('"Mental health benefits per state"')
print(tabulate(result, headers=["State","Count"], tablefmt="pretty"))
