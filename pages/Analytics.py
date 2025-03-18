import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit UI
st.title("📊 Product Feedback Analytics")

# Function to fetch and combine Product & Feedback data
def fetch_data():
    try:
        conn = sqlite3.connect("db.sqlite3")  # Connect to SQLite DB
        query = """
        SELECT f.f_id, f.p_id_id, p.name AS product_name, f.rating, f.review_text, f.sentiment
        FROM analytics_feedback f
        JOIN analytics_product p ON f.p_id_id = p.p_id
        """  
        df = pd.read_sql(query, conn)  # Load into DataFrame
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Fetch Data
data = fetch_data()

if data is not None:
    st.subheader("📌 Feedback Data Overview")
    st.dataframe(data)  # Display as table

    # ----- Summary Statistics -----
    st.subheader("📊 Summary Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Total Products", data['product_name'].nunique())
    col2.metric("Total Reviews", data.shape[0])

    # Average Rating per Product
    avg_ratings = data.groupby('product_name')['rating'].mean().reset_index()

    # Number of Reviews per Product
    review_counts = data['product_name'].value_counts().reset_index()
    review_counts.columns = ['product_name', 'review_count']

    # Sentiment Distribution
    sentiment_counts = data['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']

    # ----- Select Chart Type -----
    chart_type = st.selectbox("📈 Select Chart Type:", [
        "Ratings Distribution",
        "Average Rating per Product",
        "Sentiment Analysis",
        "Number of Reviews per Product",
        "Percentage of Positive & Negative Reviews"
    ])

    # ----- Ratings Distribution -----
    if chart_type == "Ratings Distribution":
        fig, ax = plt.subplots()
        sns.histplot(data['rating'], bins=5, kde=True, ax=ax)
        ax.set_title("Ratings Distribution")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    # ----- Average Rating per Product -----
    elif chart_type == "Average Rating per Product":
        fig, ax = plt.subplots()
        sns.barplot(x=avg_ratings['product_name'], y=avg_ratings['rating'], ax=ax)
        ax.set_title("Average Rating Per Product")
        ax.set_xlabel("Product Name")
        ax.set_ylabel("Average Rating")
        ax.set_xticklabels(avg_ratings['product_name'], rotation=30, ha="right")
        st.pyplot(fig)

    # ----- Sentiment Analysis -----
    elif chart_type == "Sentiment Analysis":
        fig, ax = plt.subplots()
        sns.barplot(x=sentiment_counts['Sentiment'], y=sentiment_counts['Count'], ax=ax, palette="viridis")
        ax.set_title("Sentiment Analysis of Reviews")
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    # ----- Number of Reviews per Product -----
    elif chart_type == "Number of Reviews per Product":
        fig, ax = plt.subplots()
        sns.barplot(x=review_counts['product_name'], y=review_counts['review_count'], ax=ax)
        ax.set_title("Number of Reviews per Product")
        ax.set_xlabel("Product Name")
        ax.set_ylabel("Review Count")
        ax.set_xticklabels(review_counts['product_name'], rotation=30, ha="right")
        st.pyplot(fig)

    # ----- Percentage of Positive & Negative Reviews -----
    elif chart_type == "Percentage of Positive & Negative Reviews":
        sentiment_pie = sentiment_counts.set_index('Sentiment')
        fig, ax = plt.subplots()
        sentiment_pie.plot.pie(y='Count', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")  # Hide y-axis label
        ax.set_title("Percentage of Positive & Negative Reviews")
        st.pyplot(fig)

else:
    st.warning("⚠️ No data available. Please check your database.")
