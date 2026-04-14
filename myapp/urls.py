from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # AUTH
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='reg'),

    # MAIN PAGES
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    # ADD SERVICES
    path('add-labours/', views.add_labr, name='add_labours'),
    path('add-drivers/', views.add_driver, name='add_drivers'),

    # BOOKING
    path('bookservice/', views.book_service, name='bookservice'),
    path('bookinglist/', views.booking_list, name='bookinglist'),

    # SERVICE PROVIDERS
    path('serviceprovider/', views.service_provider, name='serviceprovider'),
    path('service-provider-detail/', views.service_provider_detail, name='service_provider_detail'),
    path('list-service-provider/<int:service_provider_id>/', views.view_service_provider, name='list_service_provider'),

    # CUSTOMER
    path('customer/', views.customer_details, name='customer'),

    # BOOKINGS (PROVIDER SIDE)
    path('bookings/', views.service_provider_bookings, name='bookings'),
    path('bookings/<int:booking_id>/update/', views.update_order_status, name='update_order_status'),

    # REVIEW
    path('submit-review/<int:booking_id>/', views.submit_review, name='submit_review'),

    # PAYMENT
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('process-payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),

    # COMPLAINT
    path('complaint/', views.file_complaint, name='complaint'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaint/create/<int:booking_id>/', views.create_complaint, name='create_complaint'),
    path('complaint/resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),

    # TRACKING
    path('track/', views.track_status, name='track'),
]

# MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)