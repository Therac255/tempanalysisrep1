from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = 'api_v1'
urlpatterns = [
    path('auth/', include('a12n.urls')),
    path('users/', include('users.urls')),
    path('auto/', include('auto.urls')),
    path('orders/', include('orders.urls')),
    path('seller/', include('seller.urls')),
    path('general/', include('general.urls')),
    path('buyers/', include('buyer.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('healthchecks/', include('django_healthchecks.urls')),
    path("integrations/", include("integrations.urls"))
]
