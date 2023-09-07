import requests
import json
import pandas as pd
import sqlite3,openpyxl
url = "https://alpha-vantage.p.rapidapi.com/query"
querystring = {"interval": "5min","function": "TIME_SERIES_INTRADAY","symbol": "MSFT","datatype": "json","output_size": "compact"
}
headers = {
    "X-RapidAPI-Key": "eb40ee6b8cmshe89d3a16fde484ep15bec5jsn7616fa33a4cd",
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params=querystring)
data = response.json()
time_series_data = data["Time Series (5min)"]
# Extract the first 20 records
first_20_records = dict(list(time_series_data.items())[:20])
#creating a list of dictionaries where each dictionary represents a single record
records = []
for timestamp, record in first_20_records.items():
    date,time=timestamp.split()
    record_dict = {'Date':date,"Time":time,"Open": record["1. open"],"High": record["2. high"],"Low": record["3. low"],"Close": record["4. close"],"Volume": record["5. volume"]}
    records.append(record_dict)
# Converting the list of dictionaries to a DataFrame
df = pd.DataFrame(records)
# Save the data to an Excel file
df.to_excel("stockdata_first_20_records.xlsx", index=False)
#reading excel data
my_excel_data=pd.read_excel("stockdata_first_20_records.xlsx")
#connecting to sql
con=sqlite3.connect("my_database.db")
table_name="stock_data"
my_excel_data.to_sql(table_name,con,if_exists="replace",index="False")
con.commit()
#to view the ouput open the file directory in command prompt
# Open sqlite3 databse : sqlite3 my_database.db
# query to view the data in command prompt: SELECT * FROM table_name(stock_data);


