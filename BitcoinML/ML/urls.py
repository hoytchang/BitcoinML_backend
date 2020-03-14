from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('price', views.price, name='price'),
    path('hashrate', views.hashRate, name='hashrate'),
    path('ntransactions', views.nTransactions, name='ntransactions'),
    path('nuniqueaddresses', views.nUniqueAddresses, name='nuniqueaddresses'),
    path('predict', views.predict, name='predict'),
]