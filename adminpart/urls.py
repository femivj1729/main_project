from django.urls import path
from . import views

urlpatterns=[
    path('admin_login/',views.adminlogin,name='signin'),
    path('admin/',views.adminpage,name='admin'),
    path('view/<str:username>',views.userview,name='view')
]