from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
path('load/',views.loadpage),
path('register/',views.registerpage,name='register'),
path('login/',views.loginpage,name='login'),
path('home/',views.homepage,name='home'),
path('profile/',views.profilepage,name='profile'),
path('useracc/<str:pk>',views.useraccount,name='useracc'),
path('follow/',views.followpage,name='follow'),
path('search/',views.searchpage,name='search'),
path('upload/',views.uploadpage,name='upload'),
path('like_post/<str:post_id>',views.likepage,name='like_post'),
path('delete/<str:id>',views.deletepost,name='delete'),
path('logout/',views.logoutpage,name='logout'),
path('chat/<str:username>',views.chatview,name='chat'),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
