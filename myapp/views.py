from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Driver, Labour, Complaint
from .forms import BookingForm, ReviewForm, ComplaintForm


# ---------------- HOME ----------------
def home(request):
    return render(request, 'home.html')


# ---------------- BOOK SERVICE ----------------
@login_required
def book_service(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user  # ✅ correct field
            booking.save()
            messages.success(request, "Booking created successfully")
            return redirect('bookinglist')
    else:
        form = BookingForm()

    return render(request, 'bookservice.html', {'form': form})


# ---------------- BOOKING LIST ----------------
@login_required
def booking_list(request):
    try:
        bookings = Booking.objects.filter(customer=request.user)
    except Exception:
        bookings = []

    return render(request, 'bookinglist.html', {
        'bookings': bookings
    })


# ---------------- PAYMENT ----------------
@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.is_paid = True
        booking.save()
        messages.success(request, "Payment successful")
        return redirect('bookinglist')

    return render(request, 'payment.html', {'booking': booking})


# ---------------- REVIEW ----------------
@login_required
def submit_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted")
            return redirect('bookinglist')
    else:
        form = ReviewForm()

    return render(request, 'review.html', {
        'form': form,
        'booking': booking
    })


# ---------------- COMPLAINT ----------------
@login_required
def create_complaint(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.booking = booking
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Complaint submitted")
            return redirect('bookinglist')
    else:
        form = ComplaintForm()

    return render(request, 'complaint.html', {
        'form': form,
        'booking': booking
    })


# ---------------- SERVICE PROVIDERS ----------------
@login_required
def service_provider_list(request):
    providers = Driver.objects.all() | Labour.objects.all()
    return render(request, 'service_provider_list.html', {
        'service_providers': providers
    })


# ---------------- CONTACT ----------------
def contact(request):
    if request.method == 'POST':
        messages.success(request, "Message sent successfully")

    return render(request, 'contact.html')


# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'about.html')