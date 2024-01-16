import random

from django.views import View
from django.db.models import Q, Count
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Location, Continent, Country, BucketList, ImageModel, VideoModel
 
   
class HomeView(View):
    template_name = 'base/home.html'

    def get(self, request):
        continents = Continent.objects.annotate(num_locations=Count('country__location')).all()
        locations = Location.objects.all().order_by('price')
        context = {'continents': continents, 'locations': locations}
        return render(request, self.template_name, context)
       
    
class SearchView(View):
    template_name = 'base/search.html'

    def get(self, request):
        q = request.GET.get('q', '')
        locations = Location.objects.filter(Q(name__icontains=q) |
                                            Q(continent__name__icontains=q) |
                                            Q(country__name__icontains=q))
        location_count = locations.count()
        context = {'locations': locations, 'location_count': location_count}
        return render(request, self.template_name, context)


class RegisterPage(View):
    template_name= 'base/login_register.html'
    page='register'
    
    def get(self,request):
        form = UserCreationForm()
        context={'page':self.page, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self,request):  
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
        context={'page':self.page, 'form': form}
        return render(request, self.template_name, context)

class LoginPage(View):
    template_name='base/login_register.html'
    page='login'
    
    def get(self,request):
        context= {'page':self.page}
        return render(request, self.template_name, context)
                
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('NO')
    

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('home')

class UserPage(View):
    template_name='base/user_profile.html'
    
    def get(self,request):
        form=UserForm(instance=request.user)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self,request):
        form= UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        context={'form':form}
        return render(request, self.template_name, context)

class Continent_LocationsView(View):
    template_name='base/continent_locations.html'
    def get(self,request, pk):
        continent = Continent.objects.get(id=pk)
        locations = Location.objects.filter(continent=continent)
        context = {'locations': locations, 'continent': continent}
        return render(request, self.template_name , context)

class Country_LocationsView(View):
    template_name='base/country_locations.html'
    def get(self,request, pk):
        country = Country.objects.get(id=pk)
        country_locations = Location.objects.filter(country=country)
        country_locations_count=country_locations.count()
        context = {'country_locations': country_locations, 'country': country, 'country_locations_count':country_locations_count}
        return render (request,self.template_name , context)

class LocationView(View):
    template_name='base/location.html'
    
    def get(self,request, pk):
        location = Location.objects.get(id=pk)
        location_images=ImageModel.objects.filter(location=location)
        location_videos=VideoModel.objects.filter(location=location)
        context = {'location': location, 'location_images':location_images,'location_videos':location_videos }
        return render (request, self.template_name, context)
    
    def post(self,request,pk):
        location = Location.objects.get(id=pk)
        if request.user.is_authenticated:
            if not BucketList.objects.filter(user=request.user, list_item=location).exists():
                bucket_list=BucketList(user=request.user, list_item=location)
                bucket_list.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else: 
                return HttpResponse("ALREADY IN THE LIST")
        else:
            return redirect('login')
    

def surprise(request):    
    locations= Location.objects.all()
    location_count= locations.count()
    location_id = random.randint(1,location_count) 
    surprise_location_result = Location.objects.get(id=location_id)
    context={'surprise_location_result':surprise_location_result}
    return render (request, 'base/surprise_result.html', context) 

login_required(login_url='login')
class BucketListView(View):
    template_name = 'base/bucket_list.html'
    def get(self,request,pk):
        user= User.objects.get(id=pk)
        bucket_list= BucketList.objects.filter(user=user)
        context={'user':user, 'bucket_list':bucket_list}
        return render (request, self.template_name, context)

login_required(login_url='login')
class DashboardView(View):
    template_name = 'base/dashboard.html'
    def get(self, request):
        location_form = LocationForm()
        country_form= CountryForm()
        context = {'country_form':country_form, 'location_form':location_form}
        return render(request, self.template_name, context)
        
    def post(self, request):
        if 'location_form_submit' in request.POST:
                form= LocationForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
            
        if 'country_form_submit' in request.POST:
            form= CountryForm(request.POST)
            if form.is_valid():
                form.save()

class DeleteBucketListItem(View):
    template_name= 'base/delete_page.html'
    def get(self,request, pk):
        list_item =BucketList.objects.get(id=pk)
        context={'list_item':list_item}
        return render (request, self.template_name, context)

    def post(self, request, pk):
        list_item =BucketList.objects.get(id=pk)
        list_item.delete()
        return redirect ('home')    
     