from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
rooms=[
    {'id':1,'name':'learning django'},
    { 'id':2, 'name':'learning python'},
    { 'id':3,'name':'designing UI/UX'},
]

def home(request):
    rooms=Room.objects.all()
    return render(request,'base/home.html',{'rooms':rooms})

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}

    return render(request,'base/room.html',context)

