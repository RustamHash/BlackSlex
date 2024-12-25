from django.urls import path, include

from base_app import views


app_name = 'base_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_orders/', views.show_add_orders, name='add_orders'),
    path('reports/', views.show_reports, name='reports'),
    path('processing_add_orders/', views.processing_add_orders, name='processing_add_orders'),
    path('reports/stock_wms/', views.get_stock_wms, name='stock_wms'),
    path('reports/stock_pg/', views.get_stock_pg, name='stock_pg'),
    path('reports/sverka/', views.get_sverka, name='sverka'),
    path('reports/sverka_ka/', views.get_sverka_ka, name='sverka_ka'),
]
