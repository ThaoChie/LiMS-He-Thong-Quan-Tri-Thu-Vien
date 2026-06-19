from django.urls import path
from . import views

app_name = 'circulation'

urlpatterns = [
    path('borrow/<int:book_id>/', views.borrow_request_view, name='borrow_request'),
    path('borrow/<int:pk>/cancel/', views.borrow_cancel_view, name='borrow_cancel'),
    path('borrow/<int:pk>/renew/', views.renew_borrow_view, name='renew_borrow'),
    path('history/', views.borrow_history_view, name='borrow_history'),
    path('manage/', views.manage_borrows_view, name='manage_borrows'),
    path('approve/<int:pk>/', views.approve_borrow_view, name='approve_borrow'),
    path('return/<int:pk>/', views.return_book_view, name='return_book'),
    path('pay_fine/<int:pk>/', views.pay_fine_view, name='pay_fine'),
    path('report_lost/<int:pk>/', views.report_lost_view, name='report_lost'),
    path('reserve/<int:book_id>/', views.reservation_create_view, name='reserve_book'),
    path('reservations/', views.reservation_list_view, name='reservation_list'),
    path('reservations/<int:pk>/cancel/', views.reservation_cancel_view, name='reservation_cancel'),
]
