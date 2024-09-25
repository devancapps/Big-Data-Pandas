import pandas as pd
import numpy as np

# MovieLens dataset
#Users data frame
users = pd.read_table('users.dat', sep='::', engine='python', 
                      names=['user_id', 'gender', 'age', 'occupation', 'zip'])

# Ratings dataframe
ratings = pd.read_table('ratings.dat', sep='::', engine='python', 
                        names=['user_id', 'movie_id', 'rating', 'timestamp'])

# Movies data frame
movies = pd.read_table('movies.dat', sep='::', engine='python', 
                       names=['movie_id', 'title', 'genres'])

#Merge the datasets into a single DataFrame
merged_df = ratings.merge(users, on='user_id').merge(movies, on='movie_id')

#Compute the mean ratings for each movie by gender
mean_ratings = merged_df.groupby(['movie_id', 'gender'])['rating'].mean().unstack()

# Filter out movies with fewer than 250 ratings
movie_ratings_count = merged_df['movie_id'].value_counts()
popular_movies = movie_ratings_count[movie_ratings_count >= 250].index
mean_ratings = mean_ratings.loc[popular_movies]

# Identify the top 10 movies rated highest by female viewers
top_female_movies = mean_ratings.sort_values('F', ascending=False).head(10)

#Find the movies with the most divisive ratings between male and female viewers
mean_ratings['rating_diff'] = mean_ratings['M'] - mean_ratings['F']
controversial_movies = mean_ratings.sort_values('rating_diff', key=abs, ascending=False)

#Calculate the standard deviation of ratings for each movie
rating_std = merged_df.groupby('movie_id')['rating'].std()

#Filter the standard deviation data to include only active titles
active_titles_std = rating_std[popular_movies]

#Sort standard deviation data in descending order
most_controversial = active_titles_std.sort_values(ascending=False)


print("Top 10 movies rated highest by female viewers:")
print(top_female_movies)

print("\nMovies with the most divisive ratings between male and female viewers:")
print(controversial_movies.head())

print("\nMovies with the highest rating variability:")
print(most_controversial.head())