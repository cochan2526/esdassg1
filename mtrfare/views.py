from django.shortcuts import render , redirect , get_object_or_404

from django.contrib.auth import logout
from .helper import registering_user , logging_on_user , showing_fare , showing_homepage , userORguest

# from .models import Station
from .models import BarrFac , Station , BarrCat


# Create your views here.

def homepage ( request ) :

    context = showing_homepage ( request )

    return ( render ( request , "mtrfare/index.htm" , context ) )

def barrfac ( request , station_id ) :

    username = userORguest ( request )

    station = get_object_or_404( Station , Station_ID = station_id )

    barrcat = BarrCat.objects.all ( )
    barrfac = list ( BarrFac.objects.filter ( Station = station ) )

    #
    # Build a dictionary of list of facilities grouped by category
    #

    facilities = {}

    index = len ( barrfac )
    while index :
        index = index - 1
        barrfac_item = barrfac[ index ]
        #
        #    Although the csv is trim down by filtered out all
        #    facilities not exists ( Value = "N" / False ) ,
        #    to provide compatibility , checking is kept
        #
        #    Check if the facility is exist or not
        #
        if ( barrfac_item.Value ) :
            #
            #    Get the list of the facilities grouped by the category of the item
            #
            item_cat_en = barrfac_item.BarrCat.Category_En
            item_code = barrfac_item.BarrCat.Item_Code
            facility_category = barrcat.get ( Item_Code = item_code )
            facilities_by_cat = facilities.get ( item_cat_en , [] )
            facilities_by_cat.append ( {
                "Facility_En" : facility_category.Facility_En ,
                "Adjacent_To" : barrfac_item.AJTextEn ,
                } )
            facilities [ item_cat_en ] = facilities_by_cat

    context = { "username" : username ,
                "station" : station ,
                "facilities" : facilities }

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

