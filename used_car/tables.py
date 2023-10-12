# mycar/used_car/tables.py

import django_tables2 as tables
from .models import UsedCar, charges, Customer, Payments
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html
import datetime

class UsedCarTable(tables.Table):
    total_expense = tables.Column(empty_values=(), verbose_name='Expense')
    add_expense = tables.Column(empty_values=(), verbose_name='Action')
    days_since_purchase = tables.Column(verbose_name='Days')
    
    def render_total_expense(self, record):
        total_expenses = charges.objects.filter(used_car=record).aggregate(total_expense=Sum('spares') + Sum('labour'))
        return total_expenses['total_expense'] if total_expenses['total_expense'] is not None else '—'
    
    def render_add_expense(self, record):
         add_expense_url = reverse('usedcar:create_charges', kwargs={'pk': record.pk})
         edit_car_details_url = reverse('usedcar:used_car_edit', kwargs={'pk': record.pk})
         return format_html('<a href="{}">Expense</a> | <a href="{}">Edit</a> ', add_expense_url, edit_car_details_url)

    class Meta:
        model = UsedCar
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('vehicle_name','vehicle_no', 'chassis_no', 'engine_no', 'Finance_Name', 'days_since_purchase', 'purchased_price', 'noc_received' ,'total_expense','add_expense')
        
class SoldUsedCarTable(tables.Table):
    total_expense = tables.Column(empty_values=(), verbose_name='Expense')
    days_since_purchase = tables.Column(verbose_name='Days')
    profit = tables.Column(empty_values=(), verbose_name='Profit')
    view_car_details = tables.Column(empty_values=(), verbose_name='Action')
    
    def render_view_car_details(self, record):
         view_car_details_url = reverse('usedcar:detail_view', kwargs={'pk': record.pk})
         return format_html('<a href="{}">View</a>', view_car_details_url)
    
    def render_total_expense(self, record):
        total_expenses = charges.objects.filter(used_car=record).aggregate(total_expense=Sum('spares') + Sum('labour'))
        return total_expenses['total_expense'] if total_expenses['total_expense'] is not None else 0
    
    def render_profit(self, record):
        sale_entry = Customer.objects.filter(interested_vehicle=record.pk)
        total_expenses = charges.objects.filter(used_car=record).aggregate(total_expense=Sum('spares') + Sum('labour'))['total_expense'] or 0
        return float(sale_entry[0].sell_price) - float(total_expenses) - float(record.purchased_price)

    class Meta:
        model = UsedCar
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('vehicle_name','vehicle_no', 'chassis_no', 'engine_no', 'Finance_Name', 'days_since_purchase', 'purchased_price', 'noc_received' ,'total_expense', 'profit', "view_car_details")


class CustomerTable(tables.Table):
    edit_customer = tables.Column(empty_values=(), verbose_name='Action')
    paid = tables.Column(empty_values=(), verbose_name='Paid')
    balance = tables.Column(empty_values=(), verbose_name='Balance')

    def render_edit_customer(self, record):
        add_url = reverse('usedcar:add_payments',  kwargs={'pk':record.pk})
        edit_customer = reverse('usedcar:edit_customer',  kwargs={'customer_id':record.pk})
        return format_html('<a href="{}">Add Payment</a> | <a href="{}">Edit</a>', add_url, edit_customer)
    
    def render_paid(self, record):
        payments = Payments.objects.filter(transaction_car=record).aggregate(Sum('amount'))['amount__sum'] or 0.0
        return float(payments) + float(record.advance_amount)
    
    def render_balance(self, record):
        payments = Payments.objects.filter(transaction_car=record).aggregate(Sum('amount'))['amount__sum'] or 0.0
        return float(record.sell_price) - float(payments) - float(record.advance_amount)

    class Meta:
        model = Customer 
        template_name = 'django_tables2/bootstrap4.html' 
        fields = ('name', 'contact', 'address', 'interested_vehicle', "sell_price", 'paid', 'balance')




class PaymentsTable(tables.Table):
    customer_name = tables.Column(accessor='transaction_car.name', verbose_name='Customer Name')
    customer_contact = tables.Column(accessor='transaction_car.contact', verbose_name='Customer Contact')
    customer_aadhar_no = tables.Column(accessor='transaction_car.aadhar_no', verbose_name='Customer Aadhar')
    customer_address = tables.Column(accessor='transaction_car.address', verbose_name='Customer Address')
    interested_vehicle = tables.Column(accessor='transaction_car.interested_vehicle', verbose_name='Interested Vehicle')
    sell_price = tables.Column(accessor='transaction_car.sell_price', verbose_name='Sell Price')
    advance_amount = tables.Column(accessor='transaction_car.advance_amount', verbose_name='Advance Amount')
    amount = tables.Column(verbose_name='Payment Amount')
    payment_date = tables.Column(verbose_name='Payment Date')
    total_payment = tables.Column(empty_values=(), verbose_name='Total Payment')
    
    def render_total_payment(self, record):
        return record.transaction_car.advance_amount + record.amount
    
    class Meta:
        model = Payments
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('customer_name', 'customer_contact', 'customer_address', 'interested_vehicle', 'sell_price', 'advance_amount', 'amount', 'total_payment')