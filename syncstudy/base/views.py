from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,logout, login
from django.contrib import messages #for flash messafes on login
# rooms=[
#     {'id':1,'name':'learning django'},
#     { 'id':2, 'name':'learning python'},
#     { 'id':3,'name':'designing UI/UX'},
# ]

def loginPage(request):

    page='login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # try catch block for if the user exists or not
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User Not Found')
            return
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password Not Found')
    return render(request,'base/login_register.html', context={'page':page})

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register'
    form=UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if(form.is_valid()):
            user=form.save(commit=False)
            # commit = false wont save the user directly bcoz we first need to clean the data lilbit
            user.username=user.username.lower()
            user.save()   
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Error !!!")
        
    return render(request,'base/login_register.html',context={'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request,'base/home.html',{'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages})


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    participants=room.participants.all()

    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    # getting all the children of the room (i.e. the messages)
    room_messages=room.message_set.all().order_by('-created')
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)


# if the user is not logged in, wont be able to access this page
# redirect users
@login_required(login_url='/login')
def create_room(request):
    form=RoomForm()
    if request.method=='POST':#if the request is of POST type
        form=RoomForm(request.POST)
        if(form.is_valid):# if the form is valid
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html', context)

# if the user is not logged in, wont be able to access this page
# redirect users
@login_required(login_url='/login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room')
    form=RoomForm(instance=room)
    if request.method=='POST':#if the request is of POST type
        form=RoomForm(request.POST, instance=room)# add the instance to tell which room to update
        if(form.is_valid):# if the form is valid
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html', context)

# if the user is not logged in, wont be able to access this page
# redirect users
@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    context={'obj':room}
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room')
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    context={'obj':message}
    if request.user != message.user:
        return HttpResponse('You are not allowed to update this room')
    if(request.method == 'POST'):
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)


