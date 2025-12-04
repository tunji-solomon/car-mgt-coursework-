from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib import messages
import re

# Create your views here.


def home(request):
    all_sales = Sales.objects.all()
    context = {
        "all_sales" : all_sales
    }
    print(all_sales, "HERERER")
    return render(request, "home.html", context)
    
   

def create_staff(request):
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\dA-Za-z]).{8,15}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        job_title = request.POST.get("job_type")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        print(first_name, last_name, job_title)
        context = {
                "first_name": first_name,
                "last_name": last_name,
                "job_type": job_title,
                "phone": phone,
                "email": email
            }
        
        
        if Staff.objects.filter(phone=phone).exists() == False:
            if re.match(email_pattern, email):
                if Staff.objects.filter(email=email).exists() == False:
                    if password == confirm:
                        if re.match(password_pattern, password.strip()):
                            
                            user = User.objects.create_user(username=last_name,email=email,password=password)
                            user.save()
                            new_user = Staff.objects.create(user=user,first_name=first_name, last_name=last_name,job_title=job_title.lower(), phone=phone, email=email,password=password)
                            new_user.clean_fields()
                            new_user.save()
                            user = authenticate(request, username=last_name, password=password)
                            login(request, user)
                            return redirect("home")
                            
                        else:
                            messages.info(request, "Password does not match the required pattern", extra_tags= "pattern")
                            return render(request, "create_staff.html", {"context": context})
                    else:
                        print("confirm password does not match")
                        print(context)
                        messages.info(request, "Password and confirm password mismatch", extra_tags= "mismatch")
                        return render(request, "create_staff.html", {"context":context})
                else:
                    messages.info(request, "User with email already exist", extra_tags= "email")
                    del context["email"]

                    return render(request, "create_staff.html", {"context": context})
            else:
                messages.info(request, "Email not a valid email", extra_tags="valid-email")
                context["email"] = email
                return render(request, "create_staff.html", {"context": context})

        else:
            print("user with phone already exist")
            messages.info(request, "User with phone already exist", extra_tags= "phone")
            del context["phone"]
            return render(request, "create_staff.html", {"context": context})
        
        
    return render(request, "create_staff.html")

def login_staff(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)           

            return redirect('home')
        else:
            messages.error(request, "Invalid credentials", extra_tags="wrong_credentials")
    return render(request,'home.html')


def logout_staff(request):
    logout(request)
    return redirect("home")  

def register_customer(request):
    
     customers = Customer.objects.all()
     email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
     if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        
        print(customers, "AT THE TOP")

        context = {
                "customers": customers,
                "first_name": first_name,
                "last_name": last_name,
                "address": address,
                "city": city,
                "postcode": postcode,
                "phone": phone,
                "email": email
            }
        
        
        if Staff.objects.filter(phone=phone).exists() == False:
            if re.match(email_pattern, email):
                if Customer.objects.filter(email=email).exists() == False:
              
                    
                    new_customer = Customer.objects.create(first_name=first_name, last_name=last_name,address=address, city=city, phone=phone, email=email)
                    new_customer.clean_fields()
                    new_customer.save()
                    return redirect("register-customer")

              
                else:
                    messages.info(request, "Customer with email already exist", extra_tags= "email")
                    del context["email"]

                    return render(request, "customer.html", {"context": context})
            else:
                messages.info(request, "Email not a valid email", extra_tags="valid-email")
                context["email"] = email
                return render(request, "customer.html", {"context": context})

        else:
            print("Customer with phone already exist")
            messages.info(request, "Customer with phone already exist", extra_tags= "phone")
            del context["phone"]
            return render(request, "customer.html", {"context": context})
        
    
     customer = Customer.objects.all()  
     return render(request, "customer.html", {"customers": customer})
    
        
    
        

def add_car(request):
    if request.method == "POST":
        car_make = request.POST.get("make")
        car_model = request.POST.get("model")
        car_year = request.POST.get("year")
        car_colour = request.POST.get("colour")
        car_mileage = request.POST.get("mileage")
        car_transmission = request.POST.get("transmission")
        car_price = request.POST.get("price")
        
        new_car = Car.objects.create(make=car_make, model=car_model, year=car_year, colour=car_colour,
                            mileage=car_mileage, transmission=car_transmission, price=car_price)
        
        new_car.clean_fields()
        new_car.save()
                
        return redirect("home")
    
    return render(request, "add_car.html")


def sell_car(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            staff_id = Staff.objects.get(email = request.user.email )
            customer_id = request.POST.get("customer_id")
            car_id = request.POST.get("car_id")
            payment_method = request.POST.get("payment_method")
            
            context = {
                "car_id": car_id,
                "customer_id": customer_id,
                "payment_method": payment_method
            }
            
            try:
                validate_customer_id = Customer.objects.get(customer_id=customer_id)
                validate_car_id = Car.objects.get(car_id=car_id)
            except Exception:
                messages.info(request, "Customer with ID does not exist", extra_tags="customer")
                return render(request, "sell_car.html", context)
            
            if validate_customer_id:
                del context["customer_id"]
                if validate_car_id:
                    del context["car_id"]
                    if validate_car_id.status == "Available":
                        sales_price = validate_car_id.price
                
                
                        new_car_sale = Sales.objects.create(car_id=validate_car_id, Customer_id=validate_customer_id, 
                                                            Staff_id=staff_id, sales_price=sales_price, payment_method=payment_method )
                        new_car_sale.clean_fields()
                        new_car_sale.save()
                        
                        validate_car_id.status = "Sold"
                        validate_car_id.save()
                        return redirect("home")
                    else:
                        messages.info(request, "Car has been sold, Please check another", extra_tags="carID")
                        return render(request, "sell_car.html", context)
                        
                else:
                    messages.info(request, "Car ID is invalid, Please input the right value ", extra_tags="carID")
                    return render(request, "sell_car.html", context)
            else:
                
                    messages.info(request, "Customer ID is invalid, Please input the right value ", extra_tags="customerID")
            return render(request, "sell_car", context)
        
    return render(request, "sell_car.html")

def dashboard(request):
    if request.method == "POST":
        search_by = request.POST.get("search-by")
        date = request.POST.get("date")
        query = request.POST.get("query")
        context = {
            "search_by": search_by,
            "date": None if not date else date,
            "query": None if not query else query
        }
        
        print(search_by, "SEARCH BYYYY")
        
        if search_by == "Cars available for sale":
            available_cars = Car.objects.filter(status="Available")
            context["cars"] = available_cars
            
            return render(request, "available_car.html",context )

        if search_by == "Sales by date":
            if date:
                sales_by_date =Sales.objects.filter(sales_date=date)
                if sales_by_date:
                    context["sales_by_date"]= sales_by_date
                else:
                    messages.info(request, "No sales for the above date...")
                return render(request, "home.html", context)
            else:
                messages.info(request, "Date not selected", extra_tags="date")
                
        if search_by == "Sales by staff member":
            if query:
                sales_by_staff =Sales.objects.filter(Staff_id=query)
                if sales_by_staff:
                    context["sales_by_staff"] = sales_by_staff
                else:
                    messages.info(request, "No sales made by the given staff yet...")
                return render(request, "home.html", context)
            else:
                messages.info(request, "Staff ID must be entered", extra_tags="date")
                return render(request, "home.html", context)
                
        if search_by == "Total sales revenue":
            total_sales = Sales.objects.all()
            total = 0
            if total_sales and len(total_sales) > 0:
                for sales in total_sales:
                    total += sales.sales_price
                context["total_sales"] = total
                return render(request, "total_sales.html", context)
            else:
                messages.info(request, "No sales has been made yet", extra_tags="total_sales")
                return render(request, "home.html", context)                
            
    
    return redirect("home")

def service(request):
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        staff_id = request.POST.get("staff_id")
        service_date = request.POST.get("service_date")
        service_type = request.POST.get("service_type")
        service_cost = request.POST.get("service_cost")
        service_note = request.POST.get("service_note")
        print(service_note, "servicececececec")
        
        car_instance = Car.objects.get(car_id=car_id)
        staff_instance = Staff.objects.get(staff_id=staff_id)
        
        new_service = Service.objects.create(car_id=car_instance, Staff_id=staff_instance, service_date=service_date, service_type=service_type,
                                             service_cost=service_cost, service_note=service_note)
        
        new_service.clean_fields()
        new_service.save()
        
        return redirect("service")
    
    return render(request, "service.html")
   
            
        
        
    
        
            
            
        


        
