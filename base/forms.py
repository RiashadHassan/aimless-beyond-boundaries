from django.forms import ModelForm
from .models import User, Location

class UserForm(ModelForm):
    
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {
            'username':None 
            }
        
        

class LocationForm(ModelForm):
    class Meta:
        model= Location
        fields = '__all__'
        