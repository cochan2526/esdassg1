from django.shortcuts import render , redirect , get_object_or_404

from django.contrib.auth import logout
from .helper import registering_user , logging_on_user , showing_fare , showing_homepage

from .models import Station

# Create your views here.

def homepage ( request ) :

    context = showing_homepage ( request )

    return ( render ( request , "mtrfare/index.htm" , context ) )

def barrfac ( request , station_id ) :

    station = get_object_or_404( Station , Station_ID = station_id )
    print ( station.Station_ID )
    context = { "station" : station }
    return ( render ( request , "mtrfare/barrfac.htm" , context ) )

def showfare ( request ) :

    context = showing_fare ( request )

    return ( render ( request , "mtrfare/showfare.htm" , context ) )

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

