from django.db import models


# Create your models here.


# Destination Model
class Destiny(models.Model):
    country = models.CharField(max_length=100)
    description = models.TextField()
    price_range = models.CharField(max_length=50)
    image = models.ImageField(upload_to='destiny')

    def __str__(self):
        return self.country


class Attraction(models.Model):
    place = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='attract')
    created = models.DateTimeField(auto_now_add=True)
    upload = models.DateTimeField(auto_now=True)
    destiny = models.ForeignKey(Destiny, on_delete=models.CASCADE)

    def __str__(self):
        return self.place


# Accommodation Model
class Accommodation(models.Model):
    destiny = models.ForeignKey(Destiny, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)
    description = models.TextField()
    image = models.ImageField(upload_to='accommodation/')

    def __str__(self):
        return self.name


# models.py
class Facility(models.Model):
    name = models.CharField(max_length=100)


class RoomImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, related_name='room_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accommodations/rooms/')
    facilities = models.ManyToManyField(Facility, related_name='room_images')  # Link facilities to each room image
