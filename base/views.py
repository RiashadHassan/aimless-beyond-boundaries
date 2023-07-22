from django.shortcuts import render, redirect, HttpResponse
from .models import Location, Continent, Country, BucketList, ImageModel, VideoModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LocationForm
import random

def home(request):
    #continents = Continent.objects.all()
    continents = Continent.objects.annotate(num_locations=Count('country__location')).all()
    locations=Location.objects.all().order_by('price')[:5]
    
    context = {'continents': continents,'locations':locations}
    return render(request, 'base/home.html', context)

def search(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    locations = Location.objects.filter(Q(name__icontains=q) |
                                        Q(continent__name__icontains=q) |
                                        Q(country__name__icontains=q))
    location_count = locations.count()
    context = {'locations': locations, 'location_count': location_count}
    return render(request, 'base/search.html', context)

def registerPage(request):
    page='register'
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
    context={'page':page, 'form': form}
    return render(request, 'base/login_register.html', context)


def loginPage(request):
    page='login'
        
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('NO')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def userPage(request):
    form=UserForm(instance=request.user)
    if request.method== "POST":
        form= UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request, 'base/user_profile.html', context=context)


def continentLocations(request, pk):
    continent = Continent.objects.get(id=pk)
    locations = Location.objects.filter(continent=continent)
    context = {'locations': locations, 'continent': continent}
    return render(request, 'base/continent_locations.html', context)

def countryLocations(request, pk):
    country = Country.objects.get(id=pk)
    country_locations = Location.objects.filter(country=country)
    country_locations_count=country_locations.count()
    context = {'country_locations': country_locations, 'country': country, 'country_locations_count':country_locations_count}
    return render (request, 'base/country_locations.html', context)

def location(request, pk):
    location = Location.objects.get(id=pk)
    location_images=ImageModel.objects.filter(location=location)
    location_videos=VideoModel.objects.filter(location=location)
    
    if request.method=="POST":
        if request.user.is_authenticated:
            if not BucketList.objects.filter(user=request.user, list_item=location).exists():
                bucket_list=BucketList(user=request.user, list_item=location)
                bucket_list.save()
            else: 
                return HttpResponse("ALREADY IN THE LIST")
        else:
            return redirect('login')
    context = {'location': location, 'location_images':location_images,'location_videos':location_videos }
    return render(request, 'base/location.html', context)

def surprise(request):    
    locations= Location.objects.all()
    location_count= locations.count()
    location_id = random.randint(1,location_count) 
    surprise_location_result = Location.objects.get(id=location_id)
    context={'surprise_location_result':surprise_location_result}
    return render (request, 'base/surprise_result.html', context) 

def bucketList(request,pk):
    if request.user.is_authenticated:
         user= User.objects.get(id=pk)
         bucket_list= BucketList.objects.filter(user=user)
    
    else:  
        return redirect('login')
   
    context={'user':user, 'bucket_list':bucket_list}
    return render (request, 'base/bucket_list.html', context)

def dashboard(request):
    if request.user.is_staff:
        form = LocationForm()
        
        
        if request.method == 'POST':
            
            if 'add_location' in request.POST:
                form= LocationForm(request.POST)
                if form.is_valid():
                    form.save()
                
    else:
        return redirect('home')
        
    context={'form':form}
    return render(request, 'base/dashboard.html', context)
