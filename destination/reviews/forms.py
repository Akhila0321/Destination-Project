from django import forms
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i}') for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        label="Rating (1-5)"
    )

    class Meta:
        model = Review
        fields = ['rating', 'review_text']
