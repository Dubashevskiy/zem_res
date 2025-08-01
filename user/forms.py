from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile




class UserRegisterForm(UserCreationForm):
    GENDER_CHOICES = [
        ('male', 'Чоловіча'),
        ('female', 'Жіноча'),
    ]
    username = forms.CharField(
        required=True, 
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть логін'})
        )
    email = forms.EmailField(
        required=False, 
        label='Електронна адреса',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть електронну адресу'})
        )
    password1 = forms.CharField(
        required=True, 
        label='Введіть пароль', 
        help_text='Пароль не має бути простим',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})
        )
    password2 = forms.CharField(
        required=True, 
        label='Підтвердіть пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False, 
        label='стать',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    subscribe = forms.BooleanField(
        required=False,
        label='Підписатися на розсилку',
        widget=forms.CheckboxInput()
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender']

class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(
        required=True, 
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть логін'})
        )
    email = forms.EmailField(
        required=False, 
        label='Електронна адреса',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть електронну адресу'})
        )
    

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileImageForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Чоловіча'),
        ('female', 'Жіноча'),
    ]

    img = forms.ImageField(
        label='Завантажити фото',
        required=False,
        widget = forms.FileInput
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False, 
        label='стать',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    subscribe = forms.BooleanField(
        required=False,
        label='Підписатися на розсилку',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Profile
        fields = ['img', 'gender', 'subscribe']


