from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Menu_item,Order,Order_management,Restaurant_details
from .forms import NameForm
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import ast
d1={}
#print(d1)

def registration(request):
	if 'id' in request.session:
		del request.session['id']
		message = "Session Deleted Successfully"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)
	else:
		return render(request,'remoteordering/Registration.html')


def index(request):
	if 'id' in request.session:
		return render(request,"remoteordering/index.html")
	else:
		try:
			TableNo = request.POST['TableNo']
			request.session['id'] = TableNo
			return render(request,"remoteordering/index.html")
		except:
			message = "Sorry!Table Not Registered"
			context = {'message': message }
			return render(request,'remoteordering/Registration.html',context)

		
		

	
def detail(request):
		l1=[]
		l2=[]
		if 'id' in request.session:
			if 'Name' not in request.session:

				TableNo = request.session['id']
				print()
				menu_items = Menu_item.objects.all()
				#print(menu_items)
				for item in menu_items:
					l1.append(item.Category)
					l2.append(item.Sub_Category)
				l1 = list(set(l1))
				l2 = list(set(l2))
				context = {"menu_items":menu_items,"l1":l1,'l2':l2,'TableNo':TableNo}
				return render(request,"remoteordering/detail.html",context)
			else:
				TableNo = request.session['id']
				Name = request.session['Name']
				menu_items = Menu_item.objects.all()
				#print(menu_items)
				for item in menu_items:
					l1.append(item.Category)
					l2.append(item.Sub_Category)
				l1 = list(set(l1))
				l2 = list(set(l2))
				context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2,'name':Name}
				return render(request,"remoteordering/detail.html",context)
		else:
			message = "Sorry!Table Not Registered"
			context = {'message': message }
			return render(request,'remoteordering/Registration.html',context)

def search(request):
	l1=[]
	l2=[]
	menu_items = Menu_item.objects.all()
	TableNo = request.session['id']
		#print(menu_items)
	for item in menu_items:
		l1.append(item.Category)
		l2.append(item.Sub_Category)
	l1 = list(set(l1))
	l2 = list(set(l2))
	#print(l2)
	s = request.POST['Category']
	s1=request.POST['Sub_Category']
	#print(list(request.POST.values()))
	if 'id' in request.session:
		if 'Name' in request.session:
			Cust_Name = request.session['Name']
			if s=='All':
				if s1=='All':
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2,"name": Cust_Name}
					return render(request,"remoteordering/detail.html",context)
				else:
					menu_items = Menu_item.objects.filter(Sub_Category__startswith=s1)
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2,"name": Cust_Name}
					return render(request,"remoteordering/detail.html",context)
			else:
				if s1=='All':
					menu_items = Menu_item.objects.filter(Category__startswith  = s)
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2,"name": Cust_Name}
					return render(request,"remoteordering/detail.html",context)
				else:
					menu_items = Menu_item.objects.filter(Category__startswith  = s).filter(Sub_Category__startswith=s1)
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2,"name": Cust_Name}
					return render(request,"remoteordering/detail.html",context)
				
				
		else:
			if s=='All':
				if s1=='All':
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2}
					return render(request,"remoteordering/detail.html",context)
				else:
					menu_items = Menu_item.objects.filter(Sub_Category__startswith=s1)
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2}
					return render(request,"remoteordering/detail.html",context)
			else:
				if s1=='All':
					menu_items = Menu_item.objects.filter(Category__startswith  = s)
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2}
					return render(request,"remoteordering/detail.html",context)
				else:
					menu_items = Menu_item.objects.filter(Category__startswith  = s).filter(Sub_Category__startswith=s1)
					context = {"menu_items":menu_items,"TableNo":TableNo,"l1":l1,'l2':l2}
					return render(request,"remoteordering/detail.html",context)
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)

def order(request):
	if 'id' in request.session:
		l1=[]
		menu_items = Menu_item.objects.all()
		if 'Name' not in request.session:
			count=0
			TableNo = request.POST['TableNo']
			Cust_Name = request.POST['Cust_Name']
			l2 = list(request.POST.keys())
			#print(l2)
			#print(list(request.POST.values()))
			time = timezone.now()
			for key in l2:
				if key.startswith('item'):
					count+=1
					Item_id = request.POST[key]
					print(Item_id)
					Item = Menu_item.objects.get(pk = Item_id)
					name = Item.Item_name
					status = Item.Status
					if status=='Item_Available':
						qty='quantity'+str(Item_id)
						print(qty)
						quantity = request.POST[qty]#print(type(request.POST))
						print(quantity)
						quantity = int(quantity)		
						order = Order_management(Table_No = TableNo ,Name = Cust_Name, Item_id= Item_id ,Item_name = name,Quantity = quantity, Time_of_order = time,Status = "Order Recieved" )
						order.save()
						request.session['Name'] = Cust_Name
					else:
						message = 'Sorry! '+name+' is Out Of Stock'
						context = {"menu_items":menu_items,"TableNo":TableNo,'message':message}
						return render(request,"remoteordering/detail.html",context)

			if count==0:
				message = "Please Select Atleast One Item TO Order"
				context = {"menu_items":menu_items,"TableNo":TableNo,'message':message}
				return render(request,"remoteordering/detail.html",context)
			else:
				return HttpResponseRedirect("orderdetails")

		else:
			count=0
			TableNo= request.session['id']
			Cust_Name = request.POST['Cust_Name']
			l2 = list(request.POST.keys())
			time = timezone.now()
			for key in l2:
				if key.startswith('item'):
					count+=1
					Item_id = request.POST[key]
					#print(Item_id)
					Item = Menu_item.objects.get(pk = Item_id)
					name = Item.Item_name
					status = Item.Status
					if status=='Item_Available':
						qty='quantity'+str(Item_id)
						#print(qty)
						quantity = request.POST[qty]#print(type(request.POST))
						#print(quantity)
						quantity = int(quantity)
						orders = Order_management.objects.filter(Table_No = TableNo).filter(Item_id = Item_id).filter(Name = Cust_Name)
						print(orders)
						if len(orders)>0:
							for order in orders:
								time = order.Time_of_order
								timediff = timezone.now()-time
								timediff = round(timediff.total_seconds()/60)
								if timediff<=5:
									#order.Name = Cust_Name
									order.Quantity = order.Quantity+quantity
									order.Time_of_order = time
									order.save()
								else:
									order = Order_management(Table_No = TableNo ,Name = Cust_Name, Item_id= Item_id ,Item_name = name,Quantity = quantity, Time_of_order = time,Status = "Order Recieved" )
									order.save()
						else:	
							order = Order_management(Table_No = TableNo ,Name = Cust_Name, Item_id= Item_id ,Item_name = name,Quantity = quantity, Time_of_order = time,Status = "Order Recieved" )
							order.save()

					else:
						message = 'Sorry! '+name+' is Out Of Stock'
						context = {"menu_items":menu_items,"TableNo":TableNo,'message':message}
						return render(request,"remoteordering/detail.html",context)
			if count==0:
				message = "You Havent choose any order"
				context = {"menu_items":menu_items,"TableNo":TableNo,'message':message}
				return render(request,"remoteordering/detail.html",context)
			else:
				return HttpResponseRedirect("orderdetails")
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)




def order_details(request):
	if 'id' in request.session:
		l1=[]
		l2=[]
		menu_items = Menu_item.objects.all()
		Table_No = request.session['id']
		if 'Name' in request.session:
			Cust_Name = request.session['Name']
			orders = Order_management.objects.filter(Table_No =Table_No).filter(Name = Cust_Name)
			if len(orders)==0:
				message = 'No Orders To Display! Kindly Choose one'
				context = {"orders":orders,"message":message}
				return render(request,'remoteordering/orderdetails.html',context)
			else:
				context = {"orders":orders}
				return render(request,'remoteordering/orderdetails.html',context)
		else:
			for item in menu_items:
				l1.append(item.Category)
				l2.append(item.Sub_Category)
			l1 = list(set(l1))
			l2 = list(set(l2))
			message = "You Havent Ordered Any Orders Kindly Choose One"
			context = {"menu_items":menu_items,"l1":l1,'l2':l2,'TableNo':Table_No}
			return render(request,"remoteordering/detail.html",context)
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)

		
		
def order_update(request):
	if 'id' in request.session:
		l1=[]
		l2=[]
		d1={}
		menu_items = Menu_item.objects.all()
		count=0
		for item in menu_items:
			l1.append(item.Category)
			l2.append(item.Sub_Category)
		l1 = list(set(l1))
		l2 = list(set(l2))
		TableNo = request.session['id']
		Cust_Name = request.session['Name']
		orders = Order_management.objects.filter(Table_No = TableNo).filter(Name = Cust_Name)
		#print(orders)
		for order in orders:
			print(order.Item_name)
			status  = order.Status
			time = order.Time_of_order
			timediff = timezone.now()-time
			print(timediff)
			timediff = round((timediff.total_seconds())/60)
			print(timediff)
			if timediff<=5 and status == "Order Recieved":
				count+=1
				d1[order.Item_id] = order.Quantity
		if count == 0:
			message = "Sorry!You Dont have Any Items To Update Better You Can Order New Order "
			context ={"orders":orders,"message":message}
			return render(request,"remoteordering/orderdetails.html",context)
		else:
			l3 = list(d1.keys())
			message = "These Marked Items Can Be Updated"
			context = {"menu_items":menu_items,'TableNo':TableNo,"l1":l1,'l2':l2,'l3':l3,'message':message,'d1':d1,'name':Cust_Name}
			return render(request,"remoteordering/detail.html",context)
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)

	
	"""time = order.Time_of_order
	timediff = timezone.now()-time
	timediff = round(timediff.total_seconds()/60)
	if timediff<2:
		menu_items = Menu_item.objects.all()
		context = {"menu_items":menu_items}
		return render(request,"remoteordering/detail.html",context)
	else:
		message = "Sorry!You Minium Updation time period of Two minutes expired."
		Items = ast.literal_eval(order.Items)
		context = {"order":order,'Items':Items ,'message':message}
		#return render(request,'remoteordering/orderdetails.html',context)"""
def update(request):
	TableNo = request.session['id']
	Cust_Name = request.session['Name']
	orders1 = Order_management.objects.filter(Table_No = TableNo).filter(Name = Cust_Name)
	keys = list(request.POST.keys())
	values = list(request.POST.values())
	for key in keys:
		if key.startswith('item'):
			Item_id = request.POST[key]
			orders = Order_management.objects.filter(Table_No = TableNo).filter(Item_id = Item_id)
			for order in orders:
				time = order.Time_of_order
				timediff = timezone.now()-time
				
				timediff = round(timediff.total_seconds()/60)
				print(timediff)
				if timediff<=5:
					qty='quantity'+str(Item_id)
					quantity = request.POST[qty]
					quantity = int(quantity)
					order.Quantity = quantity
					order.save()  
	context = {"orders":orders1}
	return render(request,'remoteordering/orderdetails.html',context)

def delete(request):
	 oid = request.POST['cancel']
	 Cust_Name = request.session['Name']
	 Table_No = request.session['id']
	 orders = Order_management.objects.filter(Table_No = Table_No).filter(Name = Cust_Name)
	 order = Order_management.objects.get(pk = oid)
	 time = order.Time_of_order
	 timediff = timezone.now()-time
	 timediff = round(timediff.total_seconds()/60)
	 if order.Status=='Order Recieved' and timediff<5:
	 	print(order.id)
	 	order.delete()
	 	return HttpResponseRedirect('orderdetails')
	 else:
	 	message = "Sorry!The Order Is Beyond Cancellation Stage You Cannot Cancel It"
	 	context = {"orders":orders,"message":message}
	 	return render(request,'remoteordering/orderdetails.html',context)

def orders(request):
	
		orders = Order_management.objects.filter(Status = "Order Recieved").order_by('-id')
		context = {'orders':orders}
		return render(request,"remoteordering/orders.html",context)
def order_processing(request):
	keys = request.POST.keys()
	print(list(keys))
	for key in keys:
		if key.startswith('order'):
			order = Order_management.objects.get(pk = request.POST[key])
			order.Status = "Order Dispatched"
			order.save()
	return HttpResponseRedirect("orders")
def Bill_details(request):
	if 'id' in request.session:
		if 'Name' in request.session:
			TableNo = request.session['id']
			Cust_Name = request.session['Name']
			orders = Order_management.objects.filter(Table_No = TableNo).filter(Name = Cust_Name)
			Total = 0
			d1 = {}
			for order in orders:
				if order.Status == 'Order Dispatched':
					item_id = order.Item_id
					name = order.Item_name
					quantity = order.Quantity
					price = Menu_item.objects.get(pk = item_id)
					print(price)
					price = price.Price 
					price = float(quantity * price)
					Total = Total+price
					l1=[quantity,price]
					if name in d1:
						d1[name][0] = d1[name][0]+quantity
						d1[name][1] = d1[name][1]+price
					else:
						d1[name]=l1
					
				else:
					message ="Sorry!You Haven't recieved all the orders you ordered"
					context = {'orders':orders,'message':message}
					return render(request,'remoteordering/orderdetails.html',context)
			if len(d1)>0:
				CGST = (Total*9)/100
				Total_amount = Total+2*CGST

				context = {'TableNo':TableNo,"d1":d1,'Total':Total,'CGST':CGST,'SGST':CGST,'Total_Amount':Total_amount,'name':Cust_Name}
				return render(request,'remoteordering/bill.html',context)
			else:
				message = "Sorry!You Havent Ordered Any Items To View The Bill "
				orders = Order_management.objects.filter(Table_No =TableNo)
				context = {"orders":orders,"message":message}
				return render(request,'remoteordering/orderdetails.html',context)
		else:
			return HttpResponseRedirect("detail")

		

	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)
		
def mode_of_payment(request):
	if 'id' in request.session:
		if 'Name' in request.session:
			request.session['Bill'] = request.POST["Total_Bill"]
			return render(request,"remoteordering/Payment.html")
		else:
			return HttpResponseRedirect("detail")
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)

	

def Pay(request):
	if 'id' in request.session:
		if 'Name' in request.session:
			d1={}
			Table_No= request.session['id']
			Cust_Name = request.session['Name']
			Bill_Amount = int(float(request.session['Bill']))
			orders = Order_management.objects.filter(Table_No = Table_No).filter(Name = Cust_Name)
			for order in orders:
				name = order.Item_name
				Quantity = order.Quantity
				if name in d1.keys():
					d1[name] = d1[name]+Quantity
				else:
					d1[name] = Quantity
				order.delete()
			d1 = str(d1)
			mode_of_payment = request.POST["Mode of Payment"]
			print(mode_of_payment)
			order = Order(Table_No = Table_No,Name = Cust_Name,Items = d1, Bill_Amount = Bill_Amount,Status = mode_of_payment)
			order.save()
			if mode_of_payment == 'Cash':
				message = "Thanks For Dining WIth"
				message1 = "One Of Our Serving Dept Employee Comes And Collects The Money.Kindly Collect The Bill From Him"
				context = {"message":message,"message1":message1}
				return render(request,'remoteordering/prac.html',context)
			elif mode_of_payment == "Card":

				message = "Thanks For Dining With"
				message1 = "One Of Our Serving Dept Employee Comes Along with Swiping Machine.Kindly Collect The Bill From Him"
				context = {"message":message,"message1":message1}
				return render(request,'remoteordering/prac.html',context)
			else: 
				return render(request,"remoteordering/Code.Html")
		else:
			return HttpResponseRedirect("detail")

	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)


	
def Bill_Payment(request):
	if 'id' in request.session:
		if 'Name' in request.session:
			d1={}
			Table_No= request.session['id']
			Cust_Name = request.session['Name']
			email = request.POST['email']
			subject = "Bill_Details"
			orders = Order.objects.filter(Table_No = Table_No).filter(Name = Cust_Name)
			for order in orders:
				Bill_Amount = order.Bill_Amount
				items = order.Items
				order.Status = "Paid"
				order.save()
				message = "We Thank You for Dining With The Bowl Company \n.Here are Your Bill Details\n Items:"+items+'\n'+'Bill : '+str(Bill_Amount)+"Rs"
				from_email = settings.EMAIL_HOST_USER
				to_list = [email]
				send_mail(subject,message,from_email,to_list,fail_silently = True)
			messages.success(request,"Thank You For Dining,We Hope You Revist Us Again")
			del request.session['Name']
			return HttpResponseRedirect("Tabledetails")
		else:
			return HttpResponseRedirect("detail")
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)


def new_order(request):
	if 'id' in request.session:
		if 'Name' in request.session:
			del request.session['Name']
			return HttpResponseRedirect("index")
		else:
			return HttpResponseRedirect("detail")
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)
 	
def Table_details(request):
	if 'id' in request.session:
		l1=[]
		Table_No= request.session['id']
		orders = Order_management.objects.filter(Table_No = Table_No)
		for order in orders:
			Name = order.Name
			l1.append(Name)
		l1 = list(set(l1))
		context = {"l1":l1}
		return render(request,"remoteordering/users.html",context)
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)


def user_details(request):
	if 'id' in request.session:
		Name = request.POST['Name']
		request.session['Name'] = Name
		return HttpResponseRedirect('orderdetails')
	else:
		message = "Sorry!Table Not Registered"
		context = {'message': message }
		return render(request,'remoteordering/Registration.html',context)


	
def Billing(request):
	orders = Order.objects.exclude(Status = 'Paid').order_by('-id')
	print(orders)
	context = {'orders':orders}
	return render(request,"remoteordering/Billing.html",context)











# Create your views here.
