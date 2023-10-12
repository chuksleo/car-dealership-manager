from django import forms
from .models import UsedCar , charges, Customer, Payments
from datetime import date

# class BrandForm(forms.ModelForm):
#     class Meta:
#         model = Brand
#         fields = '__all__'
        

class UsedCarForm(forms.ModelForm):
    purchased_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','max': str(date.today())}))
    class Meta:
        model = UsedCar
        fields = '__all__'
        exclude = ('status',)
        
    def __init__(self, *args, **kwargs):
        super(UsedCarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        
class ChargesForm(forms.ModelForm):
    class Meta:
        model = charges
        fields = '__all__'
        exclude = ('created_at','used_car',)
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact', 'aadhar_no' , 'address', 'interested_vehicle', 'sell_price', 'advance_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact'}),
            'aadhar_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Aadhar Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}),
            'interested_vehicle': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Interested Vehicle'}),
            'sell_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sell Price'}),
            'advance_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Advance Amount'}),
        }
        

class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'
        exclude = ('transaction_car',)
        
    def save(self, commit=True, transaction_car=None):
        instance = super().save(commit=False)
        instance.transaction_car = transaction_car
        if commit and transaction_car:
            instance.save()
        return instance