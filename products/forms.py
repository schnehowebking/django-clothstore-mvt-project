from django import forms
from .models import *

class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

STAR_CHOICES = [
    ('1', '⭐'),
    ('2', '⭐⭐'),
    ('3', '⭐⭐⭐'),
    ('4', '⭐⭐⭐⭐'),
    ('5', '⭐⭐⭐⭐⭐'),
]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=STAR_CHOICES)
    body = forms.TextInput()
    class Meta:
        model = Review
        fields = ['body', 'rating']
    def save(self, commit=True):
        review = super().save(commit=False) 
        if commit == True:
            review.save()
        return review
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'w-100 form-control border-1 py-1'
                    
                ) 
            })




class AddToWishListForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = []

