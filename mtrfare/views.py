from django.shortcuts import render , redirect

from django.contrib.auth import logout
from .helper import registering_user , logging_on_user

from .models import Station

# Create your views here.

def homepage ( request ) :
    username = request.user.username
    if ( username == "" ) :
        username = "Guest"

    source_stations = Station.objects.all ( )
    dest_stations = Station.objects.all ( )

    context = {
        "username"            : username ,
        "source_station_list" : source_stations ,
        "dest_station_list"   : dest_stations ,
    }
    return ( render ( request , "mtrfare/index.htm" , context ) )

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

