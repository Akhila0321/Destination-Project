from django.contrib.auth.models import User
from django.db import models
from tours.models import Destiny, Accommodation


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destiny = models.ForeignKey(Destiny, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.accommodation.name} from {self.check_in} to {self.check_out}'


class Book_details(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_no = models.BigIntegerField()
    pin = models.IntegerField()
    book_id = models.CharField(max_length=20, blank=True)
    booked_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default="pending")


class Payment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    book_id = models.CharField(max_length=30, blank=True)
    razorpay_payment_id = models.CharField(max_length=30, blank=True)
    paid = models.BooleanField(default=False)
