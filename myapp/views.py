from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Driver,Labour,Booking,Users,Customer,ServiceProvider,Review,Complaint
from .forms import CustomUserCreationForm, CustomAuthenticationForm, LabourForm, DriverForm, BookingForm, ContactForm,ComplaintForm
from django.utils.functional import SimpleLazyObject
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the main dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'reg.html', {'form': form})

# Service provider can add drivers and labours
@login_required
def add_labr(request):
    if request.method == 'POST':
        # Fetch the ServiceProvider associated with the logged-in user
        try:
            service_provider = ServiceProvider.objects.get(user=request.user)
        except ServiceProvider.DoesNotExist:
            return render(request, 'add_labours.html', {
                'error': "You must be logged in as a Service Provider to add a Labour."
            })

        # Create the Labour instance with form data
        Labour.objects.create(
            service_provider=service_provider,
            name=request.POST.get('name'),
            aadhar=request.POST.get('aadhar'),
            img=request.FILES.get('img'),  # Handles uploaded image
            exp=request.POST.get('exp'),
            skills=request.POST.get('skills'),
            address=request.POST.get('address'),
            phno=request.POST.get('phno'),
            availability=request.POST.get('availability') == 'on',
            rate_per_hour=request.POST.get('rate_per_hour'),
        )

        # Redirect to a success page
        return redirect('home')

    return render(request, 'add_labours.html')

@login_required

def add_driver(request):
    if request.method == 'POST':
        # Fetch the ServiceProvider associated with the logged-in user
        try:
            service_provider = ServiceProvider.objects.get(user=request.user)
        except ServiceProvider.DoesNotExist:
            return render(request, 'add_drivers.html', {
                'error': "You must be logged in as a Service Provider to add a Labour."
            })

        # Create the Driver instance with form data
        Driver.objects.create(
            service_provider=service_provider,
            name=request.POST.get('name'),
            aadhar=request.POST.get('aadhar'),
            img=request.FILES.get('img'),  # Handles uploaded image
            exp=request.POST.get('exp'),
            vehicle=request.POST.get('vehicle'),
            address=request.POST.get('address'),
            phno=request.POST.get('phno'),
            availability=request.POST.get('availability') == 'on',
            rate_per_hour=request.POST.get('rate_per_hour'),
        )

        # Redirect to a success page
        return redirect('home')

    return render(request, 'add_drivers.html')



@login_required
def service_provider(request):
    if Customer.objects.filter(user=request.user).exists():
        return render(request, 'serviceprovider.html', {'error': "Customer already exists for this user."})
    
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phno = request.POST.get('phno')

        ServiceProvider.objects.create(
            user=request.user,
            company_name=name,
            address=address,
            contact_number=phno
        )
        return redirect('home')

    return render(request, 'serviceprovider.html')


@login_required
def customer_details(request):
    if Customer.objects.filter(user=request.user).exists():
        return render(request, 'customer.html', {'error': "Customer already exists for this user."})
    
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phno = request.POST.get('phno')

        Customer.objects.create(
            user=request.user,
            name=name,
            address=address,
            phno=phno
        )
        return redirect('home')

    return render(request, 'customer.html')



def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the main dashboard
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def book_service(request):
     # Directly compare the user's role
    if request.user.role != 'customer' and not request.user.is_superuser:  # Assuming `role` is a field in your User model
        return HttpResponseForbidden("You are not authorized to book services. Please contact support.")

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user  # Assign the logged-in user as the customer
            booking.save()
            booking.calculate_cost()  # Ensure cost calculation
            return redirect('bookinglist')
    else:
        form = BookingForm()

    # Use the correct field for availability
    drivers = Driver.objects.filter(availability=True)
    labours = Labour.objects.filter(availability=True)
    
    return render(request, 'bookservice.html', {'form': form, 'drivers': drivers, 'labours': labours})



@login_required
def submit_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        serviceprovider=request.POST.get('serviceprovider')
        comment = request.POST.get('comment')
        Review.objects.create(booking=booking, rating=rating, feedback=comment, serviceprovider=serviceprovider,user=request.user)
        return redirect('home')  # Redirect to the homepage or any desired page
    return render(request, 'submitreview.html', {'booking': booking})


def file_complaint(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        complaint_text = request.POST.get('complaint_text')
        Complaint.objects.create(booking=booking, user=request.user, complaint_text=complaint_text)
    return render(request, 'complaints/file.html', {'booking': booking})

def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'bookinglist.html', {'bookings': bookings})


def track_status(request):
    status = None
    error_message = None

    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        try:
            booking = Booking.objects.get(tracking_code=tracking_code)
            status = booking.status
        except Booking.DoesNotExist:
            error_message = "No booking found with the provided tracking code."

    return render(request, 'track.html', {'status': status, 'error_message': error_message})


# Create your views here.
def home(request):
    return render(request,'home.html')

def about(request):
    reviews = Review.objects.select_related('user', 'booking').order_by('-id')[:5]  # Show the latest 5 reviews
    return render(request, 'about.html', {'reviews': reviews})
    

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for reaching out! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

@login_required
def update_order_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.service_provider != request.user:
        return HttpResponseForbidden("You are not authorized to update this booking.")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept" and booking.status == "pending":
            booking.status = "accepted"
        elif action == "decline" and booking.status == "pending":
            booking.status = "declined"
        elif action == "complete" and booking.status == "accepted":
            booking.status = "completed"
        else:
            return HttpResponseForbidden("Invalid action or status.")

        booking.save()
        return redirect("bookings")

    return HttpResponseForbidden("Invalid request.")

@login_required
def service_provider_bookings(request):
    bookings = Booking.objects.filter(service_provider=request.user).order_by("-id")
    return render(request, "bookings.html", {"bookings": bookings})

def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        # Mock payment processing logic
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Validate payment inputs
        if card_number and expiry_date and cvv:
            # Mock success scenario
            booking.status = "paid"
            booking.save()
            messages.success(request, "Payment successful!")
            return redirect('booking_details', booking_id=booking.id)
        else:
            messages.error(request, "Invalid payment details. Please try again.")

    return render(request, 'payment.html', {'booking': booking})

def view_service_provider(request, service_provider_id):
    service_provider = get_object_or_404(ServiceProvider, id=service_provider_id)
    drivers = service_provider.driver_set.all()
    laborers = service_provider.labour_set.all()
    return render(request, 'list_service_provider.html', {
        'service_provider': service_provider,
        'drivers': drivers,
        'laborers': laborers,
    })

def service_provider_detail(request):
    service_providers = ServiceProvider.objects.all()  # Fetch all service providers
    return render(request, 'service_provider_detail.html', {
        'service_providers': service_providers,
    })


def create_complaint(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    user = request.user  # Assuming the user is logged in

    if request.method == 'POST':
        # Assuming you have a ComplaintForm for validating the input
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.booking = booking
            complaint.user = user
            complaint.save()
            return redirect('complaint_list')  # Redirect to the complaint list after submission
    else:
        form = ComplaintForm()

    return render(request, 'create_complaint.html', {
        'form': form,
        'booking': booking,
    })

# View to resolve a complaint (admin only, for example)
def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.resolved = True
    complaint.save()
    return redirect('complaint_list')  # Redirect to the complaint list after resolution

def complaint_list(request):
    complaints = Complaint.objects.all()
    bookings = Booking.objects.all()  # Fetch all bookings
    return render(request, 'complaint_list.html', {
        'complaints': complaints,
        'bookings': bookings,
    })

def payment_success(request):
    transaction_id = request.GET.get("transaction_id", "N/A")
    amount_paid = request.GET.get("amount_paid", "N/A")
    booking_id = request.GET.get("booking_id", "N/A")

    return render(request, "payment_success.html", {
        "transaction_id": transaction_id,
        "amount_paid": amount_paid,
        "booking_id": booking_id,
    })

def process_payment(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)

        # Check if already paid
        if booking.is_paid:  # Assuming `is_paid` is a Boolean field
            return redirect(reverse('payment_success') + f"?already_paid=1&booking_id={booking.id}")

        if request.method == "POST":
            # Process payment logic (e.g., integrate with a payment gateway)
            transaction_id = "TXN" + str(booking.id) + "12345"  # Simulated transaction ID
            amount_paid = booking.total_cost

            # Mark booking as paid
            booking.is_paid = True
            booking.save()

            # Redirect to success page with payment details
            return redirect(reverse('payment_success') + f"?transaction_id={transaction_id}&amount_paid={amount_paid}&booking_id={booking.id}")

    except Booking.DoesNotExist:
        return HttpResponse("Invalid booking ID", status=400)

    return render(request, "payment_page.html", {"booking": booking})