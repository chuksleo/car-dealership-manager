from django.db import models
from django.urls import reverse
from django.utils import timezone

class Brand(models.Model):
    brand_name = models.CharField(max_length=50, verbose_name="Name")
    model_name = models.CharField(max_length=50, verbose_name="Model")   
    yom = models.DecimalField(max_digits=4, decimal_places=0 ,verbose_name="Year Of Manufacturing")
    
    class Meta:
        unique_together = ('brand_name', 'model_name', 'yom')
        
    def __str__(self):
        return f"{self.brand_name}|{self.model_name}|{self.yom}"

 
class UsedCar(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('advanced', 'Advanced'),
        ('sold', 'Sold'),
    )
    brand = models.ForeignKey(Brand, default=None, on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100, verbose_name="Name")
    vehicle_no = models.CharField(max_length=100, unique=True, verbose_name="Number")
    chassis_no = models.CharField(max_length=100, verbose_name="Chassis")
    engine_no = models.CharField(max_length=100, verbose_name="Engine")
    Finance_Name = models.CharField(max_length=100, verbose_name="Financer")
    purchased_date = models.DateField(default=timezone.now,  verbose_name="DOP")
    purchased_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,  verbose_name="Purchased")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available',  verbose_name="Availability")
    noc_received = models.BooleanField(verbose_name="NOC")
    comment = models.CharField(max_length=200, blank=True)
   
    def __str__(self):
        return  f"{self.vehicle_name} | {self.vehicle_no}"
    
    def get_add_expense_url(self):
        return reverse('usedcar:create_charges', args=[str(self.pk)])
    
    def days_since_purchase(self):
        current_date = timezone.now().date()
        return (current_date - self.purchased_date).days
    
class charges(models.Model):    
    used_car = models.ForeignKey(UsedCar, default=None, on_delete=models.CASCADE)
    spares = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Spare")
    labour = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Labour")
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.used_car.vehicle_name} - Spares: {self.spares}, Labour: {self.labour}"
    
    def total_expense(self):
        return self.spares + self.labour


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Customer Name")
    contact = models.CharField(max_length=10)
    aadhar_no = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    interested_vehicle = models.ForeignKey(UsedCar, on_delete=models.CASCADE, verbose_name="Vehicle")
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name
    

class Payments(models.Model):
    transaction_car = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now=True) 
