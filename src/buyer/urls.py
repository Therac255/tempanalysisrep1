from django.urls import path

from buyer.api.views import BuyerView

urlpatterns = [
    path("<uuid:pk>/get-personal-info", BuyerView.as_view({"get": "retrieve"})),
    path("<uuid:pk>/update-personal-info", BuyerView.as_view({"patch": "partial_update"})),
]
