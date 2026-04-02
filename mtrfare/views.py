from django.shortcuts import render , redirect , get_object_or_404

from django.contrib.auth import logout
from .helper import *

# from .models import Station
from .models import BarrFac , Station , BarrCat , UserPref

import json

# Create your views here.

def homepage ( request ) :

    context = showing_homepage ( request )

    return ( render ( request , "mtrfare/index.htm" , context ) )

def account ( request ) :

    username = request.user.username ;

    stations = Station.objects.all ( )

    userPrefSet = UserPref.objects.filter ( username = username )
    userPref = userPrefSet [ 0 ]

    if ( len ( userPrefSet ) == 0) :
        userPref = { "pref_source_station_id" : 0 , "pref_dest_station_id" : 0 , "Category" : [] , "Facility" : [] }

    #
    #    build the dictionary for list of barrier free facilities
    #

    barrcat = BarrCat.objects.all ( )
    facilities = {}

    index = len ( barrcat )
    while index :
        index = index - 1
        barrcat_item = barrcat[ index ]
        item_cat_en = barrcat_item.Category_En
        facilities_by_cat = facilities.get ( item_cat_en , [] )
        facilities_by_cat.append ( {
            "Item_Code" : barrcat_item.Item_Code ,
            "Category_Id" : barrcat_item.Category_Id ,
#             "Category_En" : 
#             "Category_Zh" :
            "Facility_En" : barrcat_item.Facility_En ,
#             "Facility_Zh" :
#             "Sorting_Order" :
            } )
        facilities [ item_cat_en ] = facilities_by_cat

    context = {
        "username"     : username ,
        "station_list" : stations ,
        "userPref"     : userPref ,
        "facilities"   : facilities ,
    }

#     print ( json.dumps ( { "Category" : [ "MJ" , "VJ" ] , "Facility" : [ "HJ7" , "AJ9" ] } ) )

    return ( render ( request , "mtrfare/account.htm" , context ) )

def preference ( request ) :

    username = request.user.username

# How to get checkbox values in django application
# https://stackoverflow.com/questions/48735726/how-to-get-checkbox-values-in-django-application

    for key, value in request.POST.items():
        print('Key: %s' % (key) ) 
        print ( request.POST.getlist ( "BarrCat" ) )
        print ( request.POST.getlist ( "BarrFac" ) )

    if ( len ( username ) ) :

        pref_source_station = str2int ( request.POST.get ( "Preference Source Station" , 0 ) , 0 )
        pref_dest_station = str2int ( request.POST.get ( "Preference Destionation Staion" , 0 ) , 0 )

        if ( ( pref_source_station > 0 ) or ( pref_dest_station > 0 ) ) :
            UserPref.objects.update_or_create(
                username = username ,
                defaults={
                    "pref_source_station_id" : pref_source_station ,
                    "pref_dest_station_id" : pref_dest_station ,
                    "pref_barrier_free_facilities" : json.dumps ( { "Category" : [] , "Facility" : [] } )
                },
            )

#             userPref = { "pref_source_station_id" : 0 , "pref_dest_station_id" : 0 , "Category" : [] , "Facility" : [] }
#     print ( pref_source_station , pref_dest_station )

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

