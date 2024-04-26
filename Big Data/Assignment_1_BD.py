import pymongo
import pandas 
import requests
import datetime

# Database 
df= pandas.read_csv("Top100-US.csv",sep=";")


# Connection to the API

url = "https://weatherapi-com.p.rapidapi.com/current.json"
headers = {
	"X-RapidAPI-Key": "f67045ffddmshb3c16d39f95bfb0p1b6d85jsne1fe2218bea4",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

weather_data=[]

# Connection to MongoDB Atlas
uri = "mongodb+srv://EddieConti:<password>@cluster0.ydobulw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri)

# Set up the database and the collection
db = client['Weather_Project']
collection = db['city_weather']

for index, row in df.iterrows():
    # Extract of zip_code and city name
    zip_code = row['Zip']
    city_name = row['City']
    querystring = {"q": f"{city_name},{zip_code}"}
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        weather_data = response.json()
        
        # The document we have to insert with the required format
        document = {
            "zip": zip_code,
            "city": city_name,
            "created_at": datetime.datetime.now(),
            "weather": weather_data
        }
        
        # We insert the document
        collection.insert_one(document)
    else:
        print(f"Error for zip: {zip_code} and city: {city_name}")

print("Done!")