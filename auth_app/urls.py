from django.urls import path

from auth_app import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('account/', views.accounts_view, name='account'),
    path('verify/email/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify/wOTP/', views.VerifyOTPView.as_view(), name='otp-verify'),
    path('delete/', views.del_user, name='delete'),
    path('update/', views.update_info_view, name='update'),
    path('logout/', views.user_logout, name='logout'),
    path('update/pass/', views.ChangePasswordView.as_view(), name='update-password'),
    path('update/pass/reset/', views.ResetPasswordView.as_view(), name='reset-password'),
]
