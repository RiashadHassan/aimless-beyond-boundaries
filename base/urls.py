from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.HomeView.as_view() , name = 'home'),
    
    path('login/', views.LoginPage.as_view(), name='login'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user-profile/', views.UserPage.as_view(), name='user-profile'),
    
    path('continent-locations/<str:pk>', views.Continent_LocationsView.as_view(), name= 'continent-locations'),
    path('country-locations/<str:pk>', views.Country_LocationsView.as_view(), name= 'country-locations'),
    path('location/<str:pk>', views.LocationView.as_view(), name= 'location'),
    
    path('surprise-result/', views.surprise, name='surprise'),
    path('search-result', views.SearchView.as_view(), name='search-result'),
    path('bucket-list/<str:pk>', views.BucketListView.as_view(), name= 'bucket-list'),
    
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('delete/<str:pk>', views.DeleteBucketListItem.as_view(), name='delete'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
