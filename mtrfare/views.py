from django.shortcuts import render , redirect

from django.contrib.auth import logout
from .helper import registering_user , logging_on_user

# Create your views here.

def homepage ( request ) :
    username = request.user.username
    if ( username == "" ) :
        username = "Guest"
    return ( render ( request , "mtrfare/index.htm" , { "username" : username } ) )

def register ( request ) :
    print ( "register!" )
    return ( render ( request , "mtrfare/register.htm" ) )

def registering ( request ) :

    if request.method != "POST":
        return ( redirect ("register") )

    if ( registering_user ( request ) ) :
        return ( redirect ( "homepage" ) )
    else :
        return ( redirect ("register") )

def logon ( request ) :
    return ( render ( request , "mtrfare/logon.htm" ) )

def logging_on ( request ) :

    if request.method != "POST":
        return ( redirect ("logon") )

    if ( logging_on_user ( request ) ) :
        return ( redirect ( "homepage" ) )
    else :
        return ( redirect ("logon") )

def logoff ( request ) :
    logout ( request )
    return ( redirect ( "homepage" ) )

