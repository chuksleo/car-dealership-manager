from django.urls import path
from . import views
from .views import PageView

app_name = 'usedcar'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('report/',views.report_bw_dates,name="report"),
      
    path('used_car_list/', views.used_car_list, name='used_car_list'),
    path('sold/', views.sold_list, name='sold_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:pk>/', views.used_car_detail, name='used_car_detail'),
    path('create/', views.used_car_create, name='used_car_create'),
    path('<int:pk>/edit/', views.used_car_edit, name='used_car_edit'),
    # path('<int:pk>/delete/', views.UsedCarDeleteView.as_view(), name='used_car_delete'),
    # path('<int:pk>/update/', views.used_car_update, name='used_car_update'),
    path('charges/', views.charges_list, name='charges_list'), 
    path('charges/create/<int:pk>/', views.create_charges, name='create_charges'),
    path('charges/delete/<int:pk>/', views.delete_charges, name='delete_charges'),
    path('pie-chart/', views.pie_chart_view, name='pie_chart'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:customer_id>/', views.sales_update, name='edit_customer'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('add_brand/', views.AddBrandView.as_view(), name='add_brand'),
    path('brand_list/', views.BrandListView.as_view(), name='brand_list'),
    path('<int:pk>/update_brand/', views.BrandUpdate.as_view(), name='update_brand'),
    path('<int:pk>/payments/', views.add_payments, name='add_payments'),
    path('<int:pk>/sales_detail/', PageView.as_view(), name='detail_view'),
]