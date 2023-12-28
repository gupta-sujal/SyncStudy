from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic
from .forms import RoomForm

rooms=[
    {'id':1,'name':'learning django'},
    { 'id':2, 'name':'learning python'},
    { 'id':3,'name':'designing UI/UX'},
]

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

def create_room(request):
    form=RoomForm()
    if request.method=='POST':#if the request is of POST type
        form=RoomForm(request.POST)
        if(form.is_valid):# if the form is valid
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)

    form=RoomForm(instance=room)
    if request.method=='POST':#if the request is of POST type
        form=RoomForm(request.POST, instance=room)# add the instance to tell which room to update
        if(form.is_valid):# if the form is valid
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    context={'obj':room}
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)




