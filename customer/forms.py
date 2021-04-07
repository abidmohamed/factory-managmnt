from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.gis import forms

from customer.models import Customer, City


class CityForm(ModelForm):
    class Meta:
        model = City
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name...'}),

        }
        fields = ('name',)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer

        widgets = {
            'location': forms.OSMWidget(attrs={
                'map_width': 650,
                'map_height': 400,
                'default_zoom': 3,
                'minZoom': 3,
            })
        }

        fields = ('name', 'phone', 'location', 'city', 'customer_type')
