from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('user-history/', views.user_history_view, name='user_history'),
]
