import streamlit as st
import pickle
import pandas as pd

# Load saved files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity.pkl', 'rb'))

st.title("📚 Book Recommender System")



# ---------------------------
# Section 2: Recommender
# ---------------------------
st.subheader("🎯 Find Similar Books")

# Dropdown from pivot table (all book titles)
book_list = pt.index.values
selected_book = st.selectbox("Choose a book you like:", book_list)

def recommend(book_name):
    # Find index of the book in pivot table
    index = pt.index.get_loc(book_name)
    distances = similarity_scores[index]
    book_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_books = []
    for i in book_list:
        book_title = pt.index[i[0]]
        temp_df = books[books['Book-Title'] == book_title].drop_duplicates('Book-Title')
        recommended_books.append({
            "title": temp_df['Book-Title'].values[0],
            "author": temp_df['Book-Author'].values[0],
            "image": temp_df['Image-URL-M'].values[0]
        })
    return recommended_books

if st.button("Recommend"):
    recommendations = recommend(selected_book)
    st.write("### Recommended Books:")
    for rec in recommendations:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(rec['image'], width=120)
        with col2:
            st.write(f"**{rec['title']}**")
            st.caption(f"by {rec['author']}")
