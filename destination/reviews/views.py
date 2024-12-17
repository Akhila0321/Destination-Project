from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from reviews.forms import ReviewForm

from reviews.models import Review


#
# @login_required
# def submit_review(request):
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             # Save the review with the current user
#             review = form.save(commit=False)
#             review.user = request.user  # Associate review with the current user
#             review.save()
#             return redirect('reviews:view_reviews')  # Redirect to a success page after submission
#     else:
#         form = ReviewForm()
#
#     return render(request, 'submit_review.html', {'form': form, 'stars': range(1, 6)})


@login_required
def submit_review(request):
    # Check if the user has already submitted a review
    existing_review = Review.objects.filter(user=request.user).first()

    if existing_review:
        messages.info(request, "You have already submitted a review.")
        return redirect('reviews:view_reviews')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save the review with the current user
            review = form.save(commit=False)
            review.user = request.user  # Associate the review with the current user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('reviews:view_reviews')  # Redirect to a page showing reviews
    else:
        form = ReviewForm()

    return render(request, 'submit_review.html', {'form': form, 'stars': range(1, 6)})


def view_reviews(request):
    reviews = Review.objects.all()  # Fetch all reviews from the database
    return render(request, 'view_reviews.html', {'reviews': reviews})


def travel_resources(request):
    return render(request, 'resources.html')
