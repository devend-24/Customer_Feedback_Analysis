from django.db.models import Q
from transformers import pipeline
from .models import Product, Feedback, Summary

summarizer = pipeline("summarization")

def generate_summary(product_id):
    product = Product.objects.get(id=product_id)

    positive_feedbacks = Feedback.objects.filter(product=product, sentiment="positive")
    negative_feedbacks = Feedback.objects.filter(product=product, sentiment="negative")

    positive_text = " ".join([f.review_text for f in positive_feedbacks])
    negative_text = " ".join([f.review_text for f in negative_feedbacks])

    positive_summary = summarizer(positive_text, max_length=50, min_length=20, do_sample=False)[0]["summary_text"]
    negative_summary = summarizer(negative_text, max_length=50, min_length=20, do_sample=False)[0]["summary_text"]

    Summary.objects.update_or_create(
        product=product,
        defaults={"positive_summary": positive_summary, "negative_summary": negative_summary}
    )
