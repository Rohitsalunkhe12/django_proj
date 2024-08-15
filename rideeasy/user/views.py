from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from seller.models import Car
from user.models import Detail
from django.db.models import Q
from django.contrib  import messages

# Create your views here.
cars =Car.objects.none()             #initialize global variable to store car object
filtered_cars = Car.objects.none()
def home(request):
   data={}
   global cars
   global filtered_cars
   cars= Car.objects.all()           # retrive all cars from database
   filtered_cars=cars
   user_specific_cars=Detail.objects.filter(uid=request.user.id)   # Retrieve cars in the user's cart
   print(user_specific_cars.count())
   data['cart_items']=user_specific_cars.count() 
   data['cars']=cars                           # Pass all cars to the template
   return render(request,'user/home.html',context=data)
    

def register(request):
    data={}
    is_staff=False
    if(request.method=="POST"):
        uname=request.POST['username']
        upass=request.POST['password']
        ucpass=request.POST['cpassword']
        type=request.POST['type']
        if(type=='seller'):
           is_staff=True
        if(uname=="" or upass=="" or ucpass==""): #validate user
              data['error_msg']="fields cant be empty"
              return render(request,'user/register.html',context=data)
        elif(upass!=ucpass):
              data['error_msg']="password doen not matched"
              return render(request,'user/register.html',context=data)
#from django.contrib.auth.models import User
        elif(User.objects.filter(username=uname).exists()):
           data['error_msg']=uname + " is already exist"
           return render(request,'user/register.html',context=data)
        else:
           user=User.objects.create(username=uname,is_staff=is_staff)    # Create and save new user
           user.set_password(upass)
           user.save()
           return redirect('/login')
    return render(request,'user/register.html',context=data)

def user_login(request):
    data={}
    if(request.method=="POST"):
        uname=request.POST['username']
        upass=request.POST['password']
        if(uname=="" or upass==""):
           data['error_msg']="fields cant be empty"
           return render(request,'user/login.html',context=data)
        elif(not User.objects.filter(username=uname).exists()):
            data['error_msg']=uname + " is does not exist"
            return render(request,'user/login.html',context=data)
        else:
#from django.contrib.auth import authenticate,login,logout
            user=authenticate(username=uname, password=upass)   # Log in user
            if user is None:
               data['error_msg']="Wrong password"
               return render(request,'user/login.html',context=data)
            else:
               login(request,user)    # if user register as a owner that redierect on dashboaed panel
               if(user.is_staff==True):
                 # return HttpResponse("to dashboard")
                  return redirect('/dashboard')
               else:                     # else it redirect on home page
                  return redirect('/')
    return render(request,'user/login.html')

def user_logout(request):  # request to logout
    logout(request)
    return redirect('/')

#chnage 

def add_to_cart(request,car_id):
   if(request.user.is_authenticated):
      user_id=request.user.id
      user=User.objects.get(id=user_id)
      car=Car.objects.get(id=car_id)
      # Check if the car is already in the cart
      q1 = Q(pid=car_id)
      q2 = Q(uid=user_id)
      in_cart=Detail.objects.filter(q1 & q2)
      if(in_cart.count()>0):#cart upperline
         messages.error(request,"car details alredy save in the cart")
         return redirect("/")
      else:
         cart=Detail.objects.create(uid=user, pid=car)
         cart.save()
         messages.success(request, "car details added to the cart")
         return redirect("/")
   else:
      return redirect("/login")
   
def cart_items_count(request):
   user_specific_cars=Detail.objects.filter(uid=request.user.id)
   print(user_specific_cars.count())
   user_specific_cart_count=user_specific_cars.count()
   return user_specific_cart_count
   
def cart(request):
   data={}
   total_cars=0
   total_rent=0
   cart_items=Detail.objects.filter(uid=request.user.id)
   data['cars'] = cart_items
   data['cart_items']=cart_items_count(request)
   # Calculate total items and total rent
   for item in cart_items:
      total_cars+=item.quantity
      total_rent+=(item.quantity*item.pid.rent)
   data['total_cars']=total_cars
   data['total_rent']=total_rent
   return render(request,'user/cart.html',context=data) # cart.htmllll


def update_cart_quantity(request,flag,cart_id):
   cart_items=Detail.objects.filter(id=cart_id)
   actual_qunatity=cart_items[0].quantity
   print("actual_qunatity", actual_qunatity)
   if(flag=='inc'):
      cart_items.update(quantity=actual_qunatity+1)
   else:
      if(actual_qunatity==1):
         pass
      else:
         cart_items.update(quantity=actual_qunatity-1)
   return redirect("/cart")

#filter by category logic
def filter_by_category(request,category_value):
   data={}
   global cars
   global filtered_cars
   filtered_cars=cars.filter(category=category_value)
   data['cars']=filtered_cars
   return render(request,'user/home.html',context=data)

#sort by price logic
def sort_by_price(request,flag):
   global filtered_cars
   data={}
   if(flag=='asc'):
      sorted_cars=filtered_cars.order_by('rent')
   else:
      sorted_cars=filtered_cars.order_by('-rent')
   data['cars']=sorted_cars
   return render(request,'user/home.html',context=data)

def search_by_name(request):
   data={}
   if request.method=='POST':
      car_name=request.POST.get('car_name')
      print(car_name)
      all_cars=Car.objects.all()
      searched_cars=all_cars.filter(Q(name__icontains=car_name))
      data['cars']=searched_cars
      return render(request,'user/home.html',context=data)

def delete_cart_item(request,cart_id):
   cart_item=Detail.objects.get(id=cart_id)
   cart_item.delete()
   return redirect("/cart")


def order_summary(request):
   data1={}
   total_items=0
   total_rent=0
   cart_items=Detail.objects.filter(uid=request.user.id)
   data1['cars'] = cart_items
   data1['cart_items']=cart_items_count(request)
   #getting cart items based on quantity
   for item in cart_items:
      total_items+=item.quantity
      total_rent+=(item.quantity*item.pid.rent)
   data1['total_items']=total_items
   data1['total_rent']=total_rent
   return render(request,'user/order_summary.html',context=data1)


def calculate_rent(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        rent_type = request.POST.get('rent_type')
        quantity = int(request.POST.get('quantity'))
        
        car = Car.objects.get(id=car_id)
        
        if rent_type == 'day':
            total_rent = quantity * car.rent  # Multiply by number of days
        elif rent_type == 'km':
            total_rent = quantity * car.rent  # Multiply by kilometers (if applicable)
        
        # Pass the total rent to the template
        context = {
            'car': car,
            'total_rent': total_rent,
        }
        
        return render(request, 'user/order_summary.html', context)
    else:
        return redirect('/')