from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[

   
    path('', views.user_login, name='login'),
    path('home',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('logout', views.user_logout, name='logout'),
    path('reg', views.register, name='reg'),
    path('about', views.about, name='about'),
    path('add_labours', views.add_labr, name='add_labours'),
    path('add_drivers', views.add_driver, name='add_drivers'),
    path('bookservice', views.book_service, name='bookservice'),
    path('serviceprovider', views.service_provider, name='serviceprovider'),
    path('customer', views.customer_details, name='customer'),
    path('submitreview/<int:booking_id>/', views.submit_review, name='submit_review'),
    path('bookinglist', views.booking_list, name='bookinglist'),
    path('complaint', views.file_complaint, name='complaint'),
    path('track', views.track_status, name='track'),
    path('bookings/', views.service_provider_bookings, name='bookings'),
    path('bookings/<int:booking_id>/update/', views.update_order_status, name='update_order_status'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('process-payment/', views.payment_view, name='process_payment'),
    path('service_provider_detail/', views.service_provider_detail, name='service_provider_detail'),
    path('list_service_provider/<int:service_provider_id>/', views.view_service_provider, name='list_service_provider'),  # This is the correct name for the URL
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaint/create/<int:booking_id>/', views.create_complaint, name='create_complaint'),
    path('complaint/resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path("process-payment/<int:booking_id>/", views.process_payment, name="process_payment"),
    path("payment-success/", views.payment_success, name="payment_success"), 
     
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
