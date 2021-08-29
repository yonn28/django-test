from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField( widget=forms.PasswordInput )


class RegistroForm(UserCreationForm):
	class Meta:
		model =User
		fields=[
				'username',
				'first_name',
				'last_name',
				'email',
			]
		labels ={
				'username':'Nombre de Usuario',
				'first_name':'Nombre',
				'last_name':'Apellidos',
				'email':'Correo',
		}