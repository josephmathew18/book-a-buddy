from django import forms
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Users, Labour,ServiceProvider,Customer,Driver,Booking,Complaint,Contact

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ['username', 'email', 'role']

class CustomAuthenticationForm(AuthenticationForm):
    pass

class LabourForm(forms.ModelForm):
    class Meta:
        model=Labour
        fields='__all__'

class DriverForm(forms.ModelForm):
    class Meta:
        model=Driver
        fields='__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_provider','driver', 'labour', 'date','start_time', 'end_time']  # Fields that the user can select
        widgets = {
            'driver': forms.Select(attrs={'class': 'form-control'}),
            'labour': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',
            }),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['driver'].queryset = Driver.objects.filter(availability=True)
        self.fields['labour'].queryset = Labour.objects.filter(availability=True)
        self.fields['service_provider'].queryset = Users.objects.filter(role='serviceprovider')

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError('The booking date is required.')
        if date <= now().date():
            raise forms.ValidationError('The booking date must be after today.')
        return date
        
          

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_text'] 

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone_number', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message', 'class': 'message_input'}),
        }




