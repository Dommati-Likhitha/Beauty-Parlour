from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Service, Feedback


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        # include image upload so admins can add a picture for the service
        fields = ['name', 'description', 'price', 'icon', 'image']
    
    # use clearable file input widget if you want nicer display
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.RadioSelect(),
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

