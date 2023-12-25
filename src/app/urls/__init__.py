from django.contrib import admin
from django.urls import include, path

api = [
    path('v1/', include('app.urls.v1', namespace='v1')),
]

urlpatterns = [
    path('nested-admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]
