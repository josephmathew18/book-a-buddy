from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from decimal import Decimal
import uuid

# Create your models here.

class Users(AbstractUser):
    ROLE_CHOICES = [
        ('serviceprovider', 'Service Provider'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Customer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=30, unique=True)
    phno = models.CharField(max_length=15, unique=True)


class ServiceProvider(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()



class Driver(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=12, unique=True)
    img = models.ImageField(upload_to='labour_images/', blank=True, null=True)
    exp = models.PositiveIntegerField()
    vehicle = models.CharField(max_length=25, unique=True)
    address = models.CharField(max_length=30, unique=True)
    phno = models.CharField(max_length=15, unique=True)
    availability = models.BooleanField(default=True)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
   

class Labour(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=12, unique=True)
    img = models.ImageField(upload_to='labour_images/', blank=True, null=True)
    exp = models.PositiveIntegerField()
    skills = models.CharField(max_length=25, unique=True)
    address = models.CharField(max_length=30, unique=True)
    phno = models.CharField(max_length=15, unique=True)
    availability = models.BooleanField(default=True)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class Booking(models.Model):
    customer = models.ForeignKey(Users, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    labour = models.ForeignKey(Labour, null=True, blank=True, on_delete=models.SET_NULL)
    service_provider = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, completed, canceled
    created_at = models.DateTimeField(auto_now_add=True)
    tracking_code = models.CharField(max_length=12, unique=True)
    is_paid = models.BooleanField(default=False)  # New field to track payment status

    def __str__(self):
        return f"Booking {self.id} - Paid: {self.is_paid}"

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)
    

    def calculate_cost(self):
        duration = (
            timedelta(hours=self.end_time.hour, minutes=self.end_time.minute) -
            timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)
        ).total_seconds() / 3600

        # Convert duration to Decimal for multiplication with Decimal values
        duration_decimal = Decimal(duration)

        # Initialize total_cost as a Decimal
        self.total_cost = Decimal(0)

        # Calculate total cost for driver and labour
        if self.driver:
            self.total_cost += self.driver.rate_per_hour * duration_decimal
        if self.labour:
            self.total_cost += self.labour.rate_per_hour * duration_decimal

        self.save()


    def clean(self):
        super().clean()
        errors = {}

        # Check if the date is None
        if self.date is None:
            errors['date'] = 'The booking date is required.'
        # Check if the date is in the past or today
        elif self.date <= now().date():
            errors['date'] = 'The booking date must be after today.'

        # If there are any errors, raise a single ValidationError
        if errors:
            raise ValidationError(errors)
    



class Review(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    serviceprovider = models.TextField()
    feedback = models.TextField()

    def __str__(self):
        return f"Review for booking {self.booking.id}"

class Complaint(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    complaint_text = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint for booking {self.booking.id}"


class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"

