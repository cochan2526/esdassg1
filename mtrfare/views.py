from django.shortcuts import render , redirect

from .helper import registering_user

# Create your views here.

def homepage ( request ) :
    return ( render ( request , "mtrfare/index.htm" ) )

def register ( request ) :
    return ( render ( request , "mtrfare/register.htm" ) )

def registering ( request ) :

    if request.method != "POST":
        return ( redirect ("register") )

    if ( registering_user ( request ) ) :
        return ( render ( request , "mtrfare/index.htm" ) )
    else :
        return ( redirect ("register") )


