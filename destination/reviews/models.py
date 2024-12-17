from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User model
    rating = models.IntegerField()  # Rating (out of 5, for example)
    review_text = models.TextField()  # The content of the review
    created_at = models.DateTimeField(auto_now_add=True)  # When the review was created

    def __str__(self):
        return f"Review by {self.user.username} - Rating: {self.rating}"


