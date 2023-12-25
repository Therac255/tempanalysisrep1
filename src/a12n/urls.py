from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from a12n.api.views import OtpView, UsernameTokenObtainPairView

router = DefaultRouter()
router.register(r'otp', OtpView, basename='otp')

app_name = 'a12n'

urlpatterns = [
    path('token/', UsernameTokenObtainPairView.as_view(), name='username_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
