from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('paymentgateway/', views.paymentgateway, name='paymentgateway'),
    path('success/', views.success, name='success'),

    
    path('transactions/', views.transactions, name='transactions'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>', views.notice_one, name='notice_one'),

    path('addbill/', views.addbill, name='addbill'),

    path('maintenancebill/', views.maintenancebill, name='maintenancebill'),
    path('maintenancebill/<int:pk>/', views.maintenancebill_one, name='maintenancebill_one'),


    path('memberdash/', views.memberdash, name='memberdash'),
    
    path('addnotice/', views.addnotice, name='addnotice'),
    # path('success/', views.success, name='success'),
    # path('success/', views.success, name='success'),

    




        path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="app/password_reset.html", html_email_template_name="app/mail_passwordreset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_done.html"), 
        name="password_reset_complete"),

]
