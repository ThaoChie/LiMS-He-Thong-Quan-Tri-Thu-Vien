from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.book_list_view, name='book_list'),
    path('search/', views.book_search_view, name='book_search'),
    path('book/<int:pk>/', views.book_detail_view, name='book_detail'),
    path('manage/', views.book_manage_view, name='book_manage'),
    path('manage/add/', views.book_create_view, name='book_create'),
    path('manage/import/', views.book_import_view, name='book_import'),
    path('manage/<int:pk>/edit/', views.book_edit_view, name='book_edit'),
    path('manage/<int:pk>/delete/', views.book_delete_view, name='book_delete'),
    path('categories/', views.category_manage_view, name='category_manage'),
    path('categories/<int:pk>/edit/', views.category_edit_view, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='category_delete'),
]
