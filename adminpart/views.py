from django.shortcuts import render,redirect
from socialapp.models import Profile,Post,Likepost,User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def is_admin(user):
    return user.is_superuser


def adminlogin(request):
    if request.method=='POST':
        username=request.POST['user']
        password=request.POST['pswd']
        user=authenticate(request,username=username,password=password)
        print(user)
        if user:
            login(request,user)
            return redirect('admin')
        else:
           messages.info(request,'Credential Invalid')
           return redirect('signin')
    else:
        return render(request,'adminlogin.html')



@login_required(login_url='signin')
@user_passes_test(is_admin)
def adminpage(request):
    posts=Post.objects.all()
    users=Profile.objects.all()
    likes=Likepost.objects.all()

    context={
        'posts':posts,'users':users,'likes':likes
    }
    return render(request,'adminphase.html',context)



def userview(request,username):
    user = User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    if request.user==profile.user:
        login(request,user)
    
        
    context = {
        'user': user,
        'profile': profile
        
    }
    
    return render(request,'adminview.html',context)
