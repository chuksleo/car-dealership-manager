from django.contrib import admin

from used_car.models import Brand, Customer, Payments, UsedCar, charges



# Register your models here.
admin.site.register(UsedCar)
admin.site.register(Brand)
admin.site.register(charges)

admin.site.register(Customer)
admin.site.register(Payments)



