import streamlit as st
from groq import Groq
import os
import sqlite3
import pandas as pd
import re
import matplotlib.pyplot as plt

# Set API key (ensure you set it in your environment variables)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY is not set. Please set it in your environment variables.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit UI
st.title("📝 Summary & Insights")

# Function to fetch data from SQLite
def fetch_data():
    try:
        conn = sqlite3.connect("db.sqlite3")  # Connect to SQLite DB
        query = "SELECT * FROM analytics_feedback"
        df = pd.read_sql(query, conn)  # Load data into DataFrame
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None  # Return None if there's an error

# Fetch and display data
data = fetch_data()

if data is not None:
    # Ensure correct column name
    column_name = "p_id" if "p_id" in data.columns else "p_id_id"

    # Filter reviews for Product ID 1
    reviews_input = data.loc[data[column_name] == 1, ['rating', 'review_text']]

    # Classify reviews as positive (rating >= 4) or negative (rating <= 2)
    positive_reviews = reviews_input[reviews_input['rating'] >= 4]
    negative_reviews = reviews_input[reviews_input['rating'] <= 2]

    # Count positive and negative reviews
    pos_count = len(positive_reviews)
    neg_count = len(negative_reviews)
    total_reviews = len(reviews_input)

    if total_reviews > 0:
        pos_percentage = (pos_count / total_reviews) * 100
    else:
        pos_percentage = 0

    # Define recommendation status based on positive percentage
    if pos_percentage >= 80:
        recommendation = "🌟 #Excellent Choice"
        rec_color = "green"
    elif pos_percentage >= 60:
        recommendation = "👍 #Worth Buying"
        rec_color = "blue"
    elif pos_percentage >= 40:
        recommendation = "⚖️ #Average Pick"
        rec_color = "orange"
    else:
        recommendation = "❌ #Needs Improvement"
        rec_color = "red"

    # Streamlit Layout: Donut Chart on Left, Recommendation on Right
    col1, col2 = st.columns([2, 1.5])

    with col1:
        # Create a donut chart
        fig, ax = plt.subplots()
        labels = ['Positive Reviews', 'Negative Reviews']
        sizes = [pos_count, neg_count]
        colors = ['#4CAF50', '#F44336']
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%', colors=colors,
            startangle=90, wedgeprops={'edgecolor': 'white'}
        )
        plt.setp(autotexts, size=12, weight="bold")
        ax.add_artist(plt.Circle((0, 0), 0.70, fc='white'))  # Donut hole
        st.subheader("🔍 Review Sentiment Distribution")

        st.pyplot(fig)

    with col2:
        st.markdown(f"<h3 style='color:{rec_color};'>{recommendation}</h3>", unsafe_allow_html=True)
        st.write(f"📊 **Total Reviews:** {total_reviews}")
        st.write(f"✅ **Positive Reviews:** {pos_count}")
        st.write(f"❌ **Negative Reviews:** {neg_count}")

    # Review Summary Button
    if st.button("🔍 Generate Summary"):
        if reviews_input.empty:
            st.warning("⚠️ No reviews found for Product ID 1.")
        else:
            st.info("⏳ Generating summary... Please wait.")

            # Prepare prompt
            prompt = f"Summarize these reviews into a short paragraph for positive and negative reviews separately in simple words. Finally, tell the percentage of bad reviews:\n\n{reviews_input.to_string(index=False)}"

            # API Request
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_tokens=1024,
                top_p=1
            )

            # Display summary
            summary = response.choices[0].message.content
            summary = re.sub(r"\*\*(.*?)\*\*", r"\1", summary)  # Removes **bold text**
            st.write(summary)
            st.success("✅ Summary generated successfully!")
