from django.urls import path
from .views import RetrieveDataAPIView



urlpatterns = [
    path('retrieve-data/', RetrieveDataAPIView.as_view(), name='retrieve-data'),

]