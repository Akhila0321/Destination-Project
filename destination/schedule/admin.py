from django.contrib import admin
from schedule.models import Booking,Book_details,Payment
admin.site.register(Booking)
admin.site.register(Book_details)
admin.site.register(Payment)