from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.service_list, name='services'),
    path('book/', views.book_appointment, name='book'),
    path('book/<int:service_id>/', views.book_appointment, name='book_with_service'),
    path('signup/', views.signup, name='signup'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('feedback/<int:booking_id>/', views.leave_feedback, name='leave_feedback'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('change-status/<int:booking_id>/', views.change_booking_status, name='change_booking_status'),
    # custom admin-dashboard URLs use a different prefix to avoid clashing with Django's own /admin/ patterns
    path('admin-dashboard/services/', views.service_list_admin, name='service_list_admin'),
    path('admin-dashboard/services/add/', views.service_add, name='service_add'),
    path('admin-dashboard/services/edit/<int:service_id>/', views.service_edit, name='service_edit'),
    path('admin-dashboard/services/delete/<int:service_id>/', views.service_delete, name='service_delete'),
    path('add-staff/', views.add_staff, name='add_staff'),]
