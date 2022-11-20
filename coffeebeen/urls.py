from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('coffeebeen.api_base_urls')),
    path('', admin.site.urls),

]
