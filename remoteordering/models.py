from django.db import models

# Create your models here.
class Menu_item(models.Model):
	Image_url = models.CharField(max_length = 1000)
	Category = models.CharField(max_length  = 200)
	Sub_Category = models.CharField(max_length = 200)
	Item_name = models.CharField(max_length = 250)
	Price = models.IntegerField()
	#Description = models.CharField(max_length= 500)
	Status = models.CharField(max_length = 50)
	def __str__(self):
		return self.Category+" "+self.Sub_Category
class Order(models.Model):
	#item_id = models.IntegerField()
	Table_No = models.IntegerField()
	Name = models.CharField(max_length = 250)
	Items = models.CharField(max_length = 250)
	#Quantity = models.IntegerField()
	Bill_Amount = models.IntegerField()
	Status = models.CharField(max_length = 250)
	def __str__(self):
		return "TableNO:"+str(self.Table_No)
class Order_management(models.Model):
	Table_No = models.IntegerField()
	Name = models.CharField(max_length = 250)
	Item_id = models.IntegerField()
	Item_name = models.CharField(max_length = 250)
	Quantity = models.IntegerField()
	Time_of_order = models.DateTimeField('Time of order')
	Status = models.CharField(max_length = 250)
	def __str__(self):
		return "TableNO:"+str(self.Table_No)+"/"+self.Status
class Restaurant_details(models.Model):
	No_Of_Tables = models.IntegerField()
	Restaurant_Name = models.CharField(max_length = 250)






