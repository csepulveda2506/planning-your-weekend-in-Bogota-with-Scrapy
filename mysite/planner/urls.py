from django.urls import path
from .views import SitesView

urlpatterns = [
    path('/', SitesView.as_view())
]
