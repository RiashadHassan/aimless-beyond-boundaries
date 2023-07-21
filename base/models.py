from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

class Continent(models.Model):
    name= models.CharField(max_length=15)
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    continent=models.ForeignKey(Continent, on_delete=models.CASCADE)
    name= models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
        
class Location(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    country= models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.TextField(max_length=100, unique=True)
    location_display_image=models.ImageField(upload_to='location_display_image/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, null= True, blank=True)
              
    def __str__(self):
        return self.name
    
class ImageModel(models.Model):
    location= models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_images', null=True, blank=True)
    image=models.FileField(upload_to='location_images/', null=True, blank= True)
    
    def __str__(self):
        return f'ImageModel #{self.pk}'

class VideoModel(models.Model):
    location= models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_videos', null=True, blank=True)
    video=models.FileField(upload_to='location_videos/', null=True, blank=True)
    
    def __str__(self):
        return f'VideoModel #{self.pk}'

    
class BucketList(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    list_item= models.ForeignKey(Location, on_delete=models.CASCADE)
    added_date= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.list_item.name
    
    class Meta:
        ordering=['-added_date']
    