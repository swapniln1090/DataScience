# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:26:56 2023

@author: Swapnil Nandanwar
"""



import streamlit as st
import pickle 
import os
import requests
import numpy as np


# Below are some dataframes and similarity scores that we created while training/creating recomendation system

script_directory = os.path.dirname(os.path.abspath(__file__))
popular_path = os.path.join(script_directory, 'popular.pkl')
popular_books_df = pickle.load(open(popular_path, 'rb'))

piv_tab_path = os.path.join(script_directory, 'pivot_table.pkl')
piv_tab = pickle.load(open(piv_tab_path, 'rb'))

similarity_scores_path = os.path.join(script_directory, 'similarity_scores.pkl')
similarity_scores = pickle.load(open(similarity_scores_path, 'rb'))

books_path = os.path.join(script_directory, 'books.pkl')
books = pickle.load(open(books_path, 'rb'))


st.title("Book Recommender System")
# This code Recommend the top 5 other books that are very similar to the Books User select

### Here we will write about Recommender System through which a User can select a Book and he will be given 5 Similar Book Recommendations

# Same function that we creted in Book_Recommender_Sys.ipynb

def recommender(book_name):
    
    index = np.where(piv_tab.index==book_name)[0][0]
    book_score = similarity_scores[index]
    similar_items = sorted(list(enumerate(book_score)),key = lambda x:x[1], reverse=True)[1:6] # Let's take only 5 item. Ist one is always the same book so startinging from index 1
    recommended_books = []
    # now lets get all similar items
    for i in similar_items:
        item = []
        temp_df = books[books["Book-Title"]==piv_tab.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        recommended_books.append(item)

    return recommended_books
        
         
popular_books_list = popular_books_df['Book-Title'].values

#book_images_link = popular_books_list['Image-URL-M'].values
st.markdown('<h3><strong>Select a Book of Your Interest</strong></h3>', unsafe_allow_html=True)
selected_book = st.selectbox('', popular_books_list)

# if User select some book and click on Recommend then below code
if st.button("Recommend"):
    recommendations = recommender(selected_book)
    for i in range(0, len(recommendations), 3):
        cols = st.columns(3)                    # To show 3 books in one Row
        for j, col in enumerate(cols):
            if i + j < len(recommendations):
                with col:
                    book = recommendations[i + j]
                    st.image(book[2], width=150)
                    st.write(f"**{book[0]}**")
                    st.write(f"**Author:** *{book[1]}*")


st.write(f"")
st.write(f"")
st.write(f"")

# Below Code is for Popular Books 
st.header("More Top Popular Books You can Look For...")

for i in range(0, len(popular_books_df), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(popular_books_df):
                book = popular_books_df.iloc[i + j]
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













