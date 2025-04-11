from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Product, Feedback, Summary

def get_sentiment_distribution(request, product_id):
    feedbacks = Feedback.objects.filter(product_id=product_id)
    positive = feedbacks.filter(sentiment="positive").count()
    negative = feedbacks.filter(sentiment="negative").count()
    neutral = feedbacks.filter(sentiment="neutral").count()

    return JsonResponse({"positive": positive, "negative": negative, "neutral": neutral})

def get_recommendation(request, product_id):
    recommended_product = Product.objects.exclude(id=product_id).order_by("?").first()
    return JsonResponse({"product": recommended_product.name if recommended_product else "No recommendations"})

def get_summary(request, product_id):
    summary = Summary.objects.filter(product_id=product_id).first()
    return JsonResponse({
        "positive_summary": summary.positive_summary if summary else "No data",
        "negative_summary": summary.negative_summary if summary else "No data"
    })


def home(request):
    return render(request, 'home.html', {})





# Home Page - Show all products
def product_list(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})

# Product Details Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    feedbacks = Feedback.objects.filter(p_id=product)  # Get feedbacks for this product
    return render(request, "product_detail.html", {"product": product, "feedbacks": feedbacks})

# Submit feedback via AJAX
def submit_feedback(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        rating = request.POST.get("rating")
        review_text = request.POST.get("review_text")

        product = get_object_or_404(Product, pk=product_id)
        feedback = Feedback(p_id=product, rating=rating, review_text=review_text)
        feedback.save()

        return JsonResponse({"status": "success", "message": "Feedback submitted!"})

    return JsonResponse({"status": "error", "message": "Invalid request"})

