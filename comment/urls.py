from django.urls import path,include
from . import views
urlpatterns = [
    path('updata_comment',views.update_comment, name = 'update_comment'),
]