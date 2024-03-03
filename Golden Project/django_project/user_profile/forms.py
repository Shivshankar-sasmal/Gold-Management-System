from django import forms
from django.contrib.auth.models import User

# models
from workers.models import Worker,State
from user_profile.models import Profile


# Owner Update
class UserUpdateForm(forms.ModelForm) :
    first_name = forms.CharField(label='Full Name')
    last_name = forms.ChoiceField(label='State', choices=[[i,i] for i in State.objects.all() ])

    class Meta :
        model = User
        fields = ['username','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm) :
    class Meta :
        model = Profile
        fields = ['mobile', 'aadhar_card', 'image']

# Worker Update
class Worker_UpdateForm(forms.ModelForm) :
    class Meta :
        model = User
        fields = ['username']
