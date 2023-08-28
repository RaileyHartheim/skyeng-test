from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('reviews.urls', namespace='reviews')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
