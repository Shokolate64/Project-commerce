from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,AuctionListing

class RegisterForm(UserCreationForm):
    email= forms.EmailField(required=True)

    class Meta:
        model= User
        fields= ["username", "email", "password1", "password2"]
    def clean_email(self):
        email= self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email    

class CreateListingForm(forms.ModelForm):
    class Meta:
        model= AuctionListing
        fields= ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }    