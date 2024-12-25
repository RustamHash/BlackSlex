from django.urls import path, include

from users import views

app_name = 'user'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login, name='login'),
]
