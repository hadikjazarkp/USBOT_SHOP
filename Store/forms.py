from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2',  'placeholder': 'Enter username', "id":"username"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter email', "id":"email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter password', "id":"password1"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Confirm password'}))
    
    
     
    # New field for the user's profile image
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control my-2'}))

    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2', 'profile_image']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError("Username must be at least 6 characters long.")
        if any(char.isdigit() for char in username):
            raise forms.ValidationError("Username cannot contain numbers.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@gmail.com' not in email:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
    


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = '__all__'
        widgets = {
            'expaire_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
        
# class AddressForm(forms.ModelForm):
    
#     class Meta:
#         model = Address    
#         fields = ['first_name', 'last_name', 'address_type', 'address', 'city', 'state', 'phone_number', 'pincode']    



class ImageForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField(
        max_length=10, 
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Title",
                }, 
                ),
                required=True
                )