# court/forms.py
from .models import CourtCase
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom User model

class SignUpForm(UserCreationForm):
    class Meta:
        model = User  # Point to your custom User model
        fields = ['username', 'email', 'password1', 'password2']  # Default fields


class CustomAuthenticationForm(AuthenticationForm):
    # You can add additional fields if necessary
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CourtCaseForm(forms.ModelForm):
    class Meta:
        model = CourtCase
        fields = [
            'defendant_name',
            'defendant_address',
            'crime_type',
            'crime_date',
            'crime_location',
            'arresting_officer',
            'arrest_date',
            'hearing_date',
            'adjournment_reason',
            'hearing_summary',
            'judgment_summary',
            'status',
            'judge',
            'lawyer',
            'public_prosecutor',
            'starting_date',
            'completion_date',
        ]
        widgets = {
            'crime_date': forms.DateInput(attrs={'type': 'date'}),
            'arrest_date': forms.DateInput(attrs={'type': 'date'}),
            'hearing_date': forms.DateInput(attrs={'type': 'date'}),
            'starting_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'adjournment_reason': forms.Textarea(attrs={'rows': 3}),
            'hearing_summary': forms.Textarea(attrs={'rows': 3}),
            'judgment_summary': forms.Textarea(attrs={'rows': 3}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search Cases',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter search keyword...', 'class': 'form-control'})
    )
