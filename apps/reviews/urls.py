from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('book/<int:book_id>/add/', views.review_create_view, name='review_create'),
    path('<int:pk>/edit/', views.review_edit_view, name='review_edit'),
    path('<int:pk>/delete/', views.review_delete_view, name='review_delete'),
]
