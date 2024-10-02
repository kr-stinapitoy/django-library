from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('<int:pk>/edituser', views.EditUserView.as_view(), name='edituser'),
]