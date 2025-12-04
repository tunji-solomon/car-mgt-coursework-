from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):
    
    car_id = models.CharField(primary_key=True, blank=True)
    make = models.CharField(max_length=50, blank=False)
    model = models.CharField(max_length=50, blank=False)
    year = models.IntegerField(blank=False)
    colour = models.CharField(blank=False, max_length=50)
    mileage = models.IntegerField(blank=False)
    transmission = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(blank=False)
    status = models.CharField(default="Available")
    purchase_date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwags):
        if not self.car_id:
            isExist = Car.objects.all()
            if len(isExist) > 0:
                lastID = isExist.last()
                print(lastID.car_id)
                self.car_id = lastID.car_id.split("-")[0] + "-" + str(int(lastID.car_id.split("-")[1]) + 1)

            else:
                self.car_id = "CA-1000"
        super().save(*args, **kwags)
        
    def __str__(self):
        return self.car_id
        
class Staff(models.Model):
    
    JOB_TYPES = [
        ("sales", "Sales"),
        ("services", "Services")
    ]

    staff_id = models.CharField(primary_key=True)
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    job_title = models.CharField(choices=JOB_TYPES)
    phone = models.CharField(blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False)
    
    def save(self, *args, **kwags):
        if not self.staff_id:
            isExist = Staff.objects.all()
            if len(isExist) > 0:
                lastID = isExist.last()
                print(lastID.staff_id)
                self.staff_id = lastID.staff_id.split("-")[0] + "-" + str(int(lastID.staff_id.split("-")[1]) + 1)
            else:
                self.staff_id = "ST-1000"
        super().save(*args, **kwags)
        
    def __str__(self):
        return self.staff_id
        
    
class Customer(models.Model):
    
    customer_id = models.CharField(primary_key=True, blank=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    email = models.EmailField(blank=False, unique=True)
    
    def save(self, *args, **kwags):
        if not self.customer_id:
            isExist = Customer.objects.all()
            if len(isExist) > 0:
                lastID = isExist.last()
                print(lastID.customer_id)
                self.customer_id = lastID.customer_id.split("-")[0] + "-" + str(int(lastID.customer_id.split("-")[1]) + 1)
            else:
                self.customer_id = "CUS-1000"
        super().save(*args, **kwags)
    def __str__(self):
        return self.customer_id
        
        
class Sales(models.Model):
    
    sales_id = models.CharField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    Customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    sales_date = models.DateField(auto_now_add=True)
    sales_price = models.IntegerField(blank=False)
    payment_method = models.CharField(max_length=50, blank=False)
    
    
    
    def save(self, *args, **kwags):
        if not self.sales_id:
            isExist = Sales.objects.all()
            if len(isExist) > 0:
                lastID = isExist.last()
                print(lastID.sales_id)
                self.sales_id = lastID.sales_id.split("-")[0] + "-" + str(int(lastID.sales_id.split("-")[1]) + 1)
            else:
                self.sales_id = "SA-1000"
        super().save(*args, **kwags)
        

class Service(models.Model):
    
    service_id = models.CharField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    Staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service_date = models.DateField(auto_now_add=True)
    service_type = models.CharField(blank=False)
    service_cost = models.IntegerField(blank=False)
    service_note = models.TextField()
    
    
    def save(self, *args, **kwags):
        if not self.service_id:
            isExist = Service.objects.all()
            if len(isExist) > 0:
                lastID = isExist.last()
                print(lastID.service_id)
                self.service_id = lastID.service_id.split("-")[0] + "-" + str(int(lastID.service_id.split("-")[1]) + 1)
            else:
                self.service_id = "SE-1000"
        super().save(*args, **kwags)
    
    
    
    
    
    
    
    
    
    
    
