from django.db import models

class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

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

    def __str__(self):
        return f"Review {self.f_id} for {self.p_id.name} ({self.sentiment})"
