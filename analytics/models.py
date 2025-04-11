from django.db import models
from nltk.sentiment import SentimentIntensityAnalyzer

class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE)  # FK with delete cascade
    rating = models.IntegerField()
    review_text = models.TextField()
    
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, default='neutral')
    
    def save(self, *args, **kwargs):
        #automatially classify sentiment before saving
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(self.review_text)['compound']
        if score >= 0.05:
            self.sentiment = "positive"
        elif score <= -0.05:
            self.sentiment = "negative"
        else:
            self.sentiment = "neutral"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review {self.f_id} for {self.p_id.name} ({self.sentiment})"
