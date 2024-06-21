from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout, login
from django.contrib import messages #for flash messafes on login
# rooms=[
#     {'id':1,'name':'learning django'},
#     { 'id':2, 'name':'learning python'},
#     { 'id':3,'name':'designing UI/UX'},
# ]

def loginPage(request):
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
    return render(request,'base/login_register.html', context={})

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    topics=Topic.objects.all()
    room_count=rooms.count()
    return render(request,'base/home.html',{'rooms':rooms,'topics':topics,'room_count':room_count})

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}

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
    if request.user != room.user:
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
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)




