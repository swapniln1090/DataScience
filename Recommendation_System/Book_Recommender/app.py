# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:26:56 2023

@author: swapnil nandanwar
"""

import streamlit as st
import pickle 
import os
import requests


# Below 2 lines of Code because 
script_directory = os.path.dirname(os.path.abspath(__file__))
pickle_path = os.path.join(script_directory, 'popular.pkl')

popular_books_list = pickle.load(open(pickle_path, 'rb'))
print(type(popular_books_list), popular_books_list.head())

#popular_books_list = popular_books_list['Book-Title'].values

#book_images_link = popular_books_list['Image-URL-M'].values

# Display the books

st.title("Book Recommender System")

# Below Code is for Popular Books 
st.header("Top Popular Books")

for i in range(0, len(popular_books_list), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(popular_books_list):
                book = popular_books_list.iloc[i + j]
                with col:
                    st.image(book['Image-URL-M'], width=100)
                    st.write(f"### {book['Book-Title']}")
                    st.write(f"**Author:** {book['Book-Author']}")
                    st.write(f"**Total Ratings:** {book['numberof_ratings']}")
                    st.write(f"**Average Ratings:** {book['average_rating']:.2f}")


#for index, row in popular_books_list.iterrows():
#    st.image(row['Image-URL-M'], width=100)
#    st.write(f"### {row['Book-Title']}")
#    st.write(f"**Author:** {row['Book-Author']}")
#    st.write(f"**Total Ratings:** {row['numberof_ratings']}")
#    st.write(f"**Average Ratings:** {row['average_rating']:.2f}")




#option = st.selectbox('How would you like to be contacted?', popular_books_list)

