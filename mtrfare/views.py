from django.shortcuts import render , redirect , get_object_or_404

from django.contrib.auth import logout
from .helper import *

# from .models import Station
from .models import BarrFac , Station , BarrCat

# Create your views here.

def homepage ( request ) :

    context = showing_homepage ( request )

    return ( render ( request , "mtrfare/index.htm" , context ) )

def account ( request ) :

    username = request.user.username ;

    return ( render ( request , "mtrfare/account.htm" , { "username" : username } ) )

def preference ( request ) :

    return ( redirect ( "homepage" ) )

def barrfac ( request , station_id ) :

    context = diplay_barrfac ( request , station_id )

    return ( render ( request , "mtrfare/barrfac.htm" , context ) )

def showfare ( request ) :

    context = showing_fare ( request )
    if context :
        return ( render ( request , "mtrfare/showfare.htm" , context ) )
    else :
        return ( redirect ( "homepage" ) )

def register ( request ) :

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

