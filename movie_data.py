import pandas as pd

df = pd.read_csv("movies.csv")

movies = df.to_dict("records")
print(len(movies))