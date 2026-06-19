from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
    path('', views.proposal_list_view, name='proposal_list'),
    path('create/', views.proposal_create_view, name='proposal_create'),
    path('<int:pk>/', views.proposal_detail_view, name='proposal_detail'),
    path('review/', views.review_proposals_view, name='review_proposals'),
    path('review/<int:pk>/', views.review_proposal_action_view, name='review_proposal_action'),
]
