import json
import requests
import mysql.connector

# set up MySQL connection 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="*********",
  database="anime_data"
)

cursor = mydb.cursor()

primary_table = '''
    CREATE TABLE anime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mal_id INT,
    title VARCHAR(255) NOT NULL,
    score FLOAT,
    rating VARCHAR(255),
    genres VARCHAR(255),
    themes VARCHAR(255),
    demographics VARCHAR(255),
    studios TEXT,
    ranking INT,
    synopsis TEXT
    )
'''
cursor.execute(primary_table)
anime_id = 1

# loop over anime IDs and get data from API

while(True):
  url = f"https://api.jikan.moe/v4/anime/{anime_id}/full"
  response = requests.get(url)
  data = json.loads(response.text)
  try:
    data = data["data"]

    # extract relevant information

    mal_id = data["mal_id"]
    title = data["title"]
    score = data["score"]
    rating = data["rating"]
    genres = ", ".join([genre["name"] for genre in data["genres"]])
    ranking = data["rank"]
    themes = ", ".join([theme["name"] for theme in data["themes"]])
    demographics = ", ".join([demographic["name"] for demographic in data["demographics"]])
    synopsis = data["synopsis"]
    studios = ", ".join([studio["name"] for studio in data["studios"]])

    # insert data into MySQL

    sql = "INSERT INTO anime (mal_id, title, score, rating, genres, ranking, themes, demographics, synopsis, studios) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (mal_id, title, score, rating, genres, ranking, themes, demographics, synopsis, studios)
    cursor.execute(sql, val)
    mydb.commit()
    anime_id += 1
  except KeyError:
    anime_id += 1