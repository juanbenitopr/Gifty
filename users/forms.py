from django import forms

from users.models import Profile, GENDER


class NewUserForm(forms.Form):

    username = forms.CharField(label='Username')
    mail = forms.EmailField(label='Email',widget=forms.EmailInput())
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    name_profile =forms.CharField(label='Nombre de tu perfil')
    age = forms.IntegerField()
    gender = forms.ChoiceField(label='Gender',choices=GENDER)
    name_list = forms.CharField(label='Nombre de la lista')



class LoginForm(forms.Form):

    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['owner']