from django import forms
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "price",
            "discount_price",
            "short_description",
            "long_description",
            "category",
            "image",
            "stock",
            "listed_by",
            "listed_date",  # Added listed_by
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Product title"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Original price"
            }),
            "discount_price": forms.NumberInput(attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Discount price (optional)"
            }),
            "short_description": forms.TextInput(attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Short description"
            }),
            "long_description": forms.Textarea(attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "rows": 4,
                "placeholder": "Detailed description"
            }),
            "category": forms.Select(attrs={
                "class": "form-select bg-dark text-light border-secondary"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control bg-dark text-light border-secondary"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "min": 1
            }),
            "listed_by": forms.TextInput(attrs={  # Widget for listed_by
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Your name or seller ID (optional)"
            }),
            "listed_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control bg-dark text-light border-secondary"
                }
            )
        }
        

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        discount_price = cleaned_data.get("discount_price")

        # ✅ Validation: discount must be less than price
        if discount_price and price and discount_price >= price:
            self.add_error(
                "discount_price",
                "Discount price must be less than the original price."
            )

        return cleaned_data


from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'user_image',
            'address_line',
            'pin_code',
            'state',
            'country',
            'phone_number',
            'gender',
            'age',
        ]

from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileForm(forms.ModelForm):
    user_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        widget=forms.Select(attrs={'class':'form-select'})
    )
    age = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
    )
    address_line = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line'})
    )
    pin_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pin Code'})
    )
    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'})
    )
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'user_image', 'phone_number', 'gender', 'age', 
            'address_line', 'pin_code', 'state', 'country'
        ]
