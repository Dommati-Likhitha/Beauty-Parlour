from django.contrib import admin
from .models import Service, Booking, Staff, Feedback


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer__username', 'service__name')
    actions = ['mark_confirmed', 'mark_cancelled']

    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_confirmed.short_description = "Mark selected bookings as confirmed"

    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_cancelled.short_description = "Mark selected bookings as cancelled"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('booking__customer__username', 'booking__service__name')
