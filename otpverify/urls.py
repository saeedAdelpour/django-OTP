from django.urls import path, include
from .views import createAccount, verify, create, getOtp


urlpatterns = [
    # path('auth/', CreateAccount.as_view(), name='auth'),
    path('auth/', createAccount, name='auth'),
    path('verification/', verify, name='verification'),
    path('verification/create/', create, name='create'),
    path('getOtp/', getOtp, name='getOtp'),
]
