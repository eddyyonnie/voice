from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile,Project,Ratings


class SignUpForm(UserCreationForm):
    '''
    Form that extends the UserCreationForm

    Added fields are the email fields
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email= forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), max_length=64)
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}))


    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email","username","password1")


class ProfileUpdateForm(forms.ModelForm):
    '''
    Profile Update form

    Allows user to add a bio and custom avatar
    '''
    class Meta:
        model= Profile
        fields = ['avatar','bio']
        widgets ={
            'bio':forms.Textarea(attrs={'placeholder':'Bio'})
        }

class UserUpdateForm(forms.ModelForm):
    '''
    User update form.

    A user can add their first and last names
    '''
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ['first_name','last_name']

class LoginForm(AuthenticationForm):
    '''
    Login form.

    Takes username and password.
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['username','password']

class NewProjectForm(forms.ModelForm):
    '''
    New Project Form 
    
    Allows the user to post project images, description and url.
    '''

    class Meta:
        model = Project
        fields = ['image','title','description']

# class ReviewForm(forms.ModelForm):
#     '''
#     Allows registered users to post comments on projects
#     '''
#     class Meta:
#         model = Reviews
#         fields = ['text']

class RatingForm(forms.ModelForm):
    '''
    Form that allows users to rate and review projects posted by other users

    '''
 
    class Meta:
        model = Ratings
        fields = [ 'review']
