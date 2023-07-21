from django.contrib import admin
from .models import Location, Continent, BucketList, ImageModel, VideoModel, Country


admin.site.register(Continent)
admin.site.register(Location)
admin.site.register(BucketList)
admin.site.register(ImageModel)
admin.site.register(VideoModel)
admin.site.register(Country)