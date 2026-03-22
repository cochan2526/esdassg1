from django.shortcuts import render , redirect
# from .models import StoryEntry

# Create your views here.

def homepage ( request ) :
    return ( render ( request , "mtrfare/index.htm" ) )

def register ( request ) :
    return ( render ( request , "mtrfare/register.htm" ) )

def registering ( request ) :

    if request.method != "POST":
        return ( redirect ("register") )

    username = request.POST.get ( "username" , "" ).strip ( )
    password = request.POST.get ( "password" , "" ).strip ( )

    return ( render ( request , "mtrfare/index.htm" ) )

