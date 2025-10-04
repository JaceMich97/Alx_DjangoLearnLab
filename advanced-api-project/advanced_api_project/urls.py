from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # All API endpoints live under /api/
    path('api/', include('api.urls')),
]
