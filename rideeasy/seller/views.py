from django.shortcuts import render,redirect
from django.http import HttpResponse
from seller.models import Car
from django.contrib.auth.models import User
# Create your views here.
def dashboard(request):
   if(request.user.is_authenticated):
      return render(request,'seller/dashboard.html')
   else:
      return redirect("/")
   
def app_car(request):
   if(request.method=='POST'):   
      name=request.POST.get('name')
      rent=request.POST.get('price')
      owner=request.POST.get('owner','default_owner')
      model=request.POST.get('model','default_model')
      description=request.POST.get('description')
      quantity=request.POST.get('quantity')
      category=request.POST.get('category')
      image=request.FILES.get('image')
      is_available=request.POST.get('is_available') and ('is_available' in request.POST)
     
      user_id=request.user.id
      user=User.objects.get(id=user_id)
      created_cars=Car.objects.create(name=name,owner=owner,model=model,rent=rent,category=category,description=description,quantity=quantity,is_active=is_available,image=image,sid=user)
      created_cars.save
      return redirect("/dashboard/cars")
   return render(request,'seller/add_car.html')


def delete_cars(request,car_id):
   car=Car.objects.get(id=car_id) # Retrieves the car object with the given ID.
   car.delete()
   return redirect("/dashboard")

def update_cars(request,car_id):
   data={}
   car=Car.objects.filter(id=car_id)
   data['car']=car[0]
 
   if request.method=='POST':
      name=request.POST.get('name')
      rent=request.POST.get('rent')
      owner=request.POST.get('owner')
      model=request.POST.get('model')
      description=request.POST.get('description')
      quantity=request.POST.get('quantity')
      category=request.POST.get('category')
      is_available= 'is_available' in request.POST

      
      cars=Car.objects.filter(id=car_id)

      cars.update(name=name,rent=rent,owner=owner,model=model,category=category,description=description,quantity=quantity,is_active=is_available)
      
      car=Car.objects.get(id=car_id)
      from seller.forms import ImageForm
      import os
      form=ImageForm(request.POST, request.FILES,instance=car)
      if form.is_valid():
         image_path=car.image.path
         if(os.path.exists(image_path)): #Checks if a new image is uploaded, deletes the old one, and saves the new image using a form.
            os.remove(image_path)
         form.save()
      return redirect('/dashboard/cars')
         
   return render(request,'seller/update_car.html',context=data)

def view_cars(request):
   data={}
   cars=Car.objects.filter(sid=request.user.id)
   data['cars']=cars
   return render(request,'seller/cars.html',context=data)

