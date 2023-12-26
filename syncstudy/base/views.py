from django.shortcuts import render
from django.http import HttpResponse

rooms=[
    {'id':1,'name':'learning django'},
    { 'id':2, 'name':'learning python'},
    { 'id':3,'name':'designing UI/UX'},
]

def home(request):
    return render(request,'base/home.html',{'rooms':rooms})

def room(request,pk):
    room=None
    for i in rooms:
        if i['id']==int(pk):
            room=i
    context={'room':room}

    return render(request,'base/room.html',context)

