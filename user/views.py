from django.shortcuts import render, redirect
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileImageForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Користувач {username} успішно створений')
            return redirect('profile')

    else:
        form = UserRegisterForm()


    return render(request, 
                  'user/reg.html',
                  {'title': 'Cторінка реєстрації',
                   'form': form
                   })


@login_required
def profile(request):
    if request.method == "POST":
        profileForm = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        updateUserForm = UserUpdateForm(request.POST, instance=request.user)
        
        if profileForm.is_valid() and updateUserForm.is_valid():
            updateUserForm.save()
            profileForm.save()

            messages.success(request, f'Ваш аккаунт успішно оновлено!')
            return redirect('profile')


    else:
        profileForm = ProfileImageForm(instance=request.user.profile)
        updateUserForm = UserUpdateForm(instance=request.user)

    data = {
        'profileForm':profileForm,
        'updateUserForm': updateUserForm
    }

    return render(request, 'user/profile.html', data)

