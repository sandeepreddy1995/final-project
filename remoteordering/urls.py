from django.urls import path
from . import views
app_name  = 'remoteordering'

urlpatterns = [path("index",views.index,name = "index"),
path("detail",views.detail,name = "detail"),
path("order",views.order,name = "order"),
path("orderdetails",views.order_details,name = "orderdetails"),
path("update",views.order_update,name = "update"),
path("orders",views.orders,name = "orders"),
path('orderprocessing',views.order_processing,name= "orderprocessing"),
path('delete',views.delete,name ="delete"),
path('Billdetails',views.Bill_details,name = "Billdetails"),
path('Search',views.search,name = "Search"),
path("updates",views.update,name = "updates"),
path("Payment",views.Bill_Payment,name = "payment"),
path("Paymentmode",views.mode_of_payment,name = "paymentmode"),
path("Pay",views.Pay,name = "Pay"),
path("neworder",views.new_order,name = "neworder"),
path("Tabledetails",views.Table_details,name = "Tabledetails"),
path("userdetails",views.user_details,name = "userdetails"),
path("Billingdetails",views.Billing,name = "Billingdetails"),
path("Registration",views.registration,name = "Registration"),]