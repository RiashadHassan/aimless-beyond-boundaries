from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.HomeView.as_view() , name = 'home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('user-profile/', views.userPage, name='user-profile'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('continent-locations/<str:pk>', views.continentLocations, name= 'continent-locations'),
    path('country-locations/<str:pk>', views.countryLocations, name= 'country-locations'),
    path('location/<str:pk>', views.location, name= 'location'),
    
    path('surprise-result/', views.surprise, name='surprise'),
    path('search-result', views.search, name='search-result'),
    path('bucket-list/<str:pk>', views.bucketList, name= 'bucket-list'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/<str:pk>', views.delete, name='delete'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
