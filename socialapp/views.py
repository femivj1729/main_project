from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from . models import Profile,Post,Likepost,FollowersCount,Message
from django.contrib import messages
from django.contrib.auth.models import User
from itertools import chain
import random


# Create your views here.

def loadpage(request):
    return render(request,'firstpage.html')


def registerpage(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password != password2:
            messages.info(request,'Password not matching')
            return redirect('register')
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()

            user_model=User.objects.get(username=username)
            new_profile=Profile.objects.create(user=user_model)
            new_profile.save()
            return redirect('/accounts/login/')
    else:
        return render(request,'registerpage.html')



def loginpage(request):
    if request.method=='POST':
        username=request.POST['user']
        password=request.POST['pswd']
        user=authenticate(request,username=username,password=password)
        print(user)
        if user:
            login(request,user)
            return redirect('/accounts/home/')
        else:
           messages.info(request,'Credential Invalid')
           return redirect('login')
    else:
        return render(request,'signinpage.html')




@login_required(login_url='login')
def profilepage(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.method=='POST':
        if request.FILES.get('image') == None:
            image=user_profile.profile_pic
            fullname=request.POST['name']
            bio=request.POST['bio']
            location=request.POST['location']
            links=request.POST['links']

            user_profile.profile_pic=image
            user_profile.fullname=fullname
            user_profile.bio=bio
            user_profile.location=location
            user_profile.links=links
            user_profile.save()

        if request.FILES.get('image')!= None:
            image=request.FILES.get('image')
            fullname=request.POST['name']
            bio=request.POST['bio']
            location=request.POST['location']
            links=request.POST['links']

            user_profile.profile_pic=image
            user_profile.fullname=fullname
            user_profile.bio=bio
            user_profile.location=location
            user_profile.links=links
            user_profile.save()
        return redirect('home')


    return render(request,'profilepage.html',{'userprofile':user_profile})


@login_required(login_url='login')
def useraccount(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    user_post_length=len(user_posts)

    follower=request.user.username
    user=pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text='unfollow'
    else:
        button_text='follow'

    user_followers=len(FollowersCount.objects.filter(user=pk))
    user_following=len(FollowersCount.objects.filter(follower=pk))


    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following
    }
    return render(request,'useraccount.html',context)




@login_required(login_url='login')
def followpage(request):
    if request.method=='POST':
        follower=request.POST['follower']
        user=request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower=FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('useracc',user)
        
        else:
            new_follower=FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('useracc',user)

    else:
        return redirect('home')
    

@login_required(login_url='login')
def searchpage(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)

    if request.method=='POST':
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username)
        
        username_profile=[]
        username_profile_list=[]

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists=Profile.objects.filter(user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list=list(chain(*username_profile_list))

    return render(request,'searchpage.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})



@login_required(login_url='login')
def homepage(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    num_post=[]
    posts_no=Post.objects.filter(user=user_object)
    for num in posts_no:
        num_post.append(num)

    user_following_list=[]
    feed=[]
    user_follower_list=[]

    user_following=FollowersCount.objects.filter(follower=request.user.username)
    user_follower=FollowersCount.objects.filter(user=request.user.username)

    for follow in user_follower:
        user_follower_list.append(follow.follower)


    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists=Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list=list(chain(*feed))

    # user suggestion starts
    all_users=User.objects.all()
    user_following_all=[]

    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list=[x for x in list(all_users) if (x not in list(user_following_all)) ]
    current_user=User.objects.filter(username=request.user.username)
    final_suggestions_list=[x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile=[]
    username_profile_list=[]
    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists=Profile.objects.filter(user=ids)
        username_profile_list.append(profile_lists)
    
    suggestions_list=list(chain(*username_profile_list))

    context={
        'userprofile':user_profile,
        'posts':feed_list,
        'suggestions_list':suggestions_list[:4],
        'user_following_list':user_following_list,
        'num_post':num_post,
        'user_follower_list':user_follower_list

    }

    return render(request,'indexpage.html',context)




@login_required(login_url='login')
def uploadpage(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('upload_files')
        caption=request.POST['caption']
        if image == None:
            messages.info(request,'select file')
            return redirect('upload')
        else:
            new_post=Post.objects.create(user=user,image=image,caption=caption)
            new_post.save()
            return redirect('home')

    else:
        return render(request,'uploadpage.html')




@login_required(login_url='login')
def likepage(request,post_id):
    username=request.user.username
    # post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)
    like_filter=Likepost.objects.filter(post_id=post_id,username=username).first()
    
    if like_filter == None:
        new_like=Likepost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('home')
    
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('home')



@login_required(login_url='login')
def deletepost(request,id):
    dele=Post.objects.get(id=id)
    
    if request.method =='POST':
        dele.delete()
        return redirect('home')
    return render(request,'deletepost.html',{'delete_post':dele})



def logoutpage(request):
    logout(request)
    return redirect('/accounts/login/')



@login_required(login_url='login')
def chatview(request,username):
    receiver=User.objects.get(username=username)
    if request.method=='POST':
        content=request.POST.get('content')
        if content.strip() != '':
            message=Message.objects.create(sender=request.user,receiver=receiver,content=content)
            message.save()
            return redirect('chat',username=username)
    messages=Message.objects.filter(sender=request.user,receiver=receiver) | Message.objects.filter(sender=receiver,receiver=request.user)
    messages=messages.order_by('timestamp')
    contex={'receiver':receiver,'messages':messages}
    return render(request,'chatview.html',contex)




   






 