from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .models import Service, Booking, Feedback
from .forms import SignUpForm, BookingForm, ServiceForm, FeedbackForm


def home(request):
    services = Service.objects.all()
    return render(request, 'salon/home.html', {'services': services})


def about(request):
    return render(request, 'salon/about.html')


def service_list(request):
    services = Service.objects.all()
    return render(request, 'salon/services.html', {'services': services})


@login_required
def book_appointment(request, service_id=None):
    initial_service = None
    if service_id:
        initial_service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            messages.success(request, 'Your appointment has been booked successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {}
        if initial_service:
            initial_data['service'] = initial_service
        form = BookingForm(initial=initial_data)
    return render(request, 'salon/booking.html', {'form': form, 'selected_service': initial_service})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'salon/signup.html', {'form': form})


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    services = Service.objects.all()
    staff = []  # staff could be retrieved via Staff model if desired
    feedbacks = Feedback.objects.select_related('booking', 'booking__customer', 'booking__service').order_by('-created_at')
    return render(request, 'salon/admin_dashboard.html', {
        'bookings': bookings,
        'services': services,
        'staff': staff,
        'feedbacks': feedbacks,
    })


@login_required
def booking_history(request):
    # retrieve bookings and prefetch feedback to avoid extra queries
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at').select_related('feedback')
    return render(request, 'salon/booking_history.html', {'bookings': bookings})


@login_required
def leave_feedback(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status != 'completed':
        messages.error(request, "You can only leave feedback for completed bookings.")
        return redirect('booking_history')
    # one-to-one relation ensures attribute access
    if hasattr(booking, 'feedback'):
        messages.info(request, "Feedback already submitted for this booking.")
        return redirect('booking_history')
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.booking = booking
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('booking_history')
    else:
        form = FeedbackForm()
    return render(request, 'salon/feedback_form.html', {'form': form, 'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status not in ['cancelled', 'completed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    return redirect('booking_history')


@user_passes_test(is_admin)
def change_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Booking.STATUS_CHOICES).keys():
            booking.status = status
            booking.save()
            messages.success(request, 'Status updated.')
        return redirect('admin_dashboard')
    return render(request, 'salon/change_status.html', {'booking': booking, 'choices': Booking.STATUS_CHOICES})


@user_passes_test(is_admin)
def service_list_admin(request):
    services = Service.objects.all()
    return render(request, 'salon/admin_services.html', {'services': services})

@user_passes_test(is_admin)
def add_staff(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            messages.success(request, 'Staff account created.')
            return redirect('admin_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'salon/add_staff.html', {'form': form})


@user_passes_test(is_admin)
def service_add(request):
    if request.method == 'POST':
        # include request.FILES to process uploaded image
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added.')
            return redirect('service_list_admin')
    else:
        form = ServiceForm()
    return render(request, 'salon/service_form.html', {'form': form, 'title': 'Add Service'})


@user_passes_test(is_admin)
def service_edit(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated.')
            return redirect('service_list_admin')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'salon/service_form.html', {'form': form, 'title': 'Edit Service'})


@user_passes_test(is_admin)
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, 'Service deleted.')
    return redirect('service_list_admin')
