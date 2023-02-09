#First Code, downloading the data from Api to CSV file
import requests
import pandas as pd

#Manual input of the Start date, end date and SE_Area to interact with the Api
#Be Aware! Only SE3 & SE4 currently works with the API
Start_date = "2021-01-01"
end_date = "2022-01-01"
SE_Area = "SE4"
url = f"https://api.energidataservice.dk/dataset/Elspotprices/download?format=json?offset=0&start={Start_date}T00:00&end={end_date}T00:00&filter=%7B%22PriceArea%22:[%22{SE_Area}%22]%7D&sort=HourUTC%20DESC&timezone=dk"
response = requests.get(url)


#Getting the data as JSON -file
def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        new_one = requests.get(url)
        data = new_one.json()
        df = pd.DataFrame(data)
        user_jsonfile = input('The name of JSON-File? ')
        df.to_json(f"{user_jsonfile}.json", index=True, orient='records')
        return user_jsonfile
    else:
        print("Error")

#Using the JSON-File,
#Dropping the SpotPriceDKK and HourUTC
#Replacing the the HourDK with TimeStamp
def clean_elpriser(File):
    df = pd.read_json(File)
    df = df.drop(['HourUTC', 'SpotPriceDKK'], axis=1)
    df['HourDK'] = df['HourDK'].str[:16]
    df['HourDK'] = df['HourDK'].str.replace('T', ' ')
    df = df.rename(columns={'HourDK': 'Timestamp'})
    df = df.drop_duplicates(subset=['Timestamp'], keep='first')
    df = df.sort_values(by=['Timestamp'])
    user_csvfile= input('The name of CSV-file? ')
    df.to_csv(f'{user_csvfile}.csv', sep=';', index=True)


#Calls the Created JSON-File
user_jsonfile = get_data(url)
clean_elpriser(user_jsonfile + ".json")



