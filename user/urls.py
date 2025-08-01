from django.urls import path
from . import views as userViews
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('reg/', userViews.register, name="reg" ),
    path('profile/', userViews.profile, name="profile"),
    path('', authViews.LoginView.as_view(template_name='user/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='user/exit.html'), name='exit'),
    path('pass_reset/', authViews.PasswordResetView.as_view(template_name='user/pass_reset.html'), name='pass_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_done/', authViews.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_complete/', authViews.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)