import os
import streamlit as st
import django
from django.conf import settings

# Configure Django settings (Only needed for Streamlit)
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=['analytics'],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
            }
        }
    )

# Setup Django
django.setup()

# Import Django models
from analytics.models import Product, Feedback

# Set wide layout
st.set_page_config(layout="wide")  

# Get absolute image paths
image_folder = os.path.abspath("images/")

# Fetch products from Django database
products = Product.objects.all()

# Apply CSS for box styling
st.markdown("""
    <style>
        .product-box {
            background-color: #f8f9fa;  
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit App
st.title("🛒 E-Commerce Store")
st.subheader("Customer Feedback Analysis Project")

# Check if a specific product is selected
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

# Display product list
if st.session_state.selected_product is None:
    for product in products:
        with st.container(border=True):
            cols = st.columns([1, 3])  # Left: Image, Right: Details

            with cols[0]:  # Image Column
                image_path = os.path.join(image_folder, f"{product.name.lower()}.jpg")
                if os.path.exists(image_path):
                    st.image(image_path, width=150)
                else:
                    st.error(f"Image not found: {image_path}")

            with cols[1]:  # Details Column
                st.subheader(product.name)
                st.write(f"**💰 Price:** ₹{product.price}")
                st.write(product.description)
                if st.button(f"🔍 View {product.name}", key=product.p_id):
                    st.session_state.selected_product = product
                    st.rerun()

# Display product details + feedback form
else:
    product = st.session_state.selected_product
    st.markdown("### 🏷️ Product Details")

    cols = st.columns([1, 3])  # Left: Image, Right: Details

    with cols[0]:  # Image Column
        image_path = os.path.join(image_folder, f"{product.name.lower()}.jpg")
        if os.path.exists(image_path):
            st.image(image_path, width=200)
        else:
            st.error(f"Image not found: {image_path}")

    with cols[1]:  # Details Column
        st.subheader(product.name)
        st.write(f"**💰 Price:** ₹{product.price}")
        st.write(product.description)

        # Feedback Form
        st.markdown("### ✍️ Leave a Review")

        rating = st.slider("Rate the product (1-5):", min_value=1, max_value=5, value=3)
        review_text = st.text_area("Write your feedback:")

        if st.button("Submit Review"):
            if review_text.strip():
                # Save feedback to the database
                feedback = Feedback(p_id=product, rating=rating, review_text=review_text)
                feedback.save()
                st.success("✅ Thank you! Your review has been submitted.")
                st.rerun()
            else:
                st.error("❌ Review text cannot be empty!")

    # Fetch and display existing reviews for this product
    st.markdown("### ⭐ Customer Reviews")
    reviews = Feedback.objects.filter(p_id=product).order_by('-f_id')  # Fetch latest reviews first

    if reviews.exists():
        for review in reviews:
            with st.container():
                st.write(f"**Rating:** {'⭐' * review.rating} ({review.rating}/5)")
                st.write(f"💬 {review.review_text}")
                st.markdown("---")
    else:
        st.info("No reviews yet. Be the first to review!")

    if st.button("🔙 Back to Products"):
        st.session_state.selected_product = None
        st.rerun()
