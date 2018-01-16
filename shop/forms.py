from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from dobwidget import DateOfBirthWidget

class SignUpForm(UserCreationForm):
    CLG_CHOICES = (
        ('MIT', 'Mahakal Institute Of Technology'),
        ('MITM', 'Mahakal Institute Of Technology And Management'),
    )
    BRANCH_CHOICES = (
        ('CS', 'Computer Science And Engineering'),
        ('IT', 'Information Technology'),
        ('CE', 'Civil Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('EC', 'Electronic Engineering'),
    )
    college = forms.ChoiceField(choices=CLG_CHOICES)
    branch = forms.ChoiceField(choices=BRANCH_CHOICES)
    birth_date = forms.DateField()
    phone = forms.CharField(max_length=10)
    username = forms.CharField(label='Roll Number', max_length=12)
    class Meta:
        model = User
        fields = ('college','branch','username','email','birth_date','phone','password1', 'password2', )


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


#login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=12,label='Roll Number')
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('college','branch','birth_date',)