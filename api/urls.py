from django.urls import path

from api import views

# app_name = 'api'

urlpatterns = [
    path('filials/', views.FilialAPIView.as_view(), name='filials'),
    path('menus/', views.MenuAPIView.as_view(), name='menu'),
    path('submenus/', views.SubMenuAPIView.as_view(), name='submenu'),
    path('tests/', views.TestViewSet.as_view(), name='tests')
]