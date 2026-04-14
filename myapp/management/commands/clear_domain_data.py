from django.core.management.base import BaseCommand
from myapp.models import Customer, ServiceProvider, Labour, Driver

class Command(BaseCommand):
    help = 'Clears all data from Customer, ServiceProvider, Labour, and Driver tables.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting records...")
        
        # We catch the count of deleted objects
        labour_count, _ = Labour.objects.all().delete()
        self.stdout.write(f"Deleted {labour_count} Labour records.")
        
        driver_count, _ = Driver.objects.all().delete()
        self.stdout.write(f"Deleted {driver_count} Driver records.")
        
        provider_count, _ = ServiceProvider.objects.all().delete()
        self.stdout.write(f"Deleted {provider_count} ServiceProvider records.")
        
        customer_count, _ = Customer.objects.all().delete()
        self.stdout.write(f"Deleted {customer_count} Customer records.")
        
        self.stdout.write(self.style.SUCCESS("Successfully cleared all requested tables!"))
