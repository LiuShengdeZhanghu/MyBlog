from django.urls import path,include
from . import views
urlpatterns = [
    path('like_change',views.like_change,name = 'like_change')
]