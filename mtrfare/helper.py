from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import BarrCat , Station , BarrFac , Fare , UserPref

import json

# Source - https://stackoverflow.com/a/6761908
# Posted by Manny D
# Retrieved 2026-03-27, License - CC BY-SA 3.0
#
#    setting __all__ for import *
#

__all__ = [ "registering_user" ,
            "logging_on_user" ,
            "showing_fare" ,
#             "userORguest" ,
            "showing_homepage" ,
            "diplay_barrfac" ,
            "str2int" ,
            "getUserPref" ,
          ]

#
#    Convert a string to integer
#        Parameters : string to be converted
#        Return : Integer converted
#                 None or value set by caller if the string is not integer
#
def str2int ( input_str , notnumber = None ) :
    try :
        value = int ( input_str )  # Try to convert string to integer
    except :
        value = notnumber    # If string is NOT int, return None or value set
    return ( value )

#
#    Return "Guest" if username is not exists ( not logged on )
#
def userORguest ( request ) :
    username = request.user.username
    if ( username == "" ) :
        username = "Guest"
    return ( username )

#
#    Get user preference
#    parameter = request
#    return preference of the user
#    or default preference if preference not set or not logged on
#
def getUserPref ( request ) :

    #
    #    set default user preference
    #
    userPref = { "Pref_source_station_id" : 0 , "Pref_dest_station_id" : 0 , "Category" : [] , "Facility" : [] }

    username = request.user.username

    if ( username != "" ) :
        #
        #    get user preference if not running as guest
        #
        userPrefSet = UserPref.objects.filter ( User = request.user )

        #
        #    restore user preference if exists
        #    as new user may have not set
        #
        if len ( userPrefSet ) :
            userPref = {}
            userPref[ "Pref_source_station_id" ] = str2int( userPrefSet [ 0 ].Pref_source_station_id )
            userPref[ "Pref_dest_station_id"   ] = str2int ( userPrefSet [ 0 ].Pref_dest_station_id )
            userPref.update( json.loads ( userPrefSet [ 0 ].Pref_barrier_free_facilities ) )

    return ( userPref )

#
#    Barrier Free Facilities of Station
#    Parameters : station
#    Return dictionary of facilities { "category" : [ List of facilities ] }
#
def station_facilities ( station_id ) :

    facilities = {}

    station = get_object_or_404( Station , Station_ID = station_id )

    barrcat = BarrCat.objects.all ( )
    barrfac = list ( BarrFac.objects.filter ( Station = station ) )

    #
    # Build a dictionary of list of facilities grouped by category
    #

    index = len ( barrfac )
    while index :
        index = index - 1
        barrfac_item = barrfac[ index ]
        #
        #    Although the csv is trimmed down by filtered out all
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

    return ( facilities )

#
#    get fare from source station to destination staion
#    parameters : source staion as Station, destination staion as Station
#    return dictionary of fare
#
def getFare ( source_station , dest_station ) :
    #
    #    In order to reduce the size of data set
    #    fare dataset has been trimmed down to half
    #    as the fare is the same from station A to station
    #    B , regardless of direction.
    #    that is only fare of station with smaller id to
    #    bigger id is stored in dataset, the full fare table
    #    for any station will be joining of from station with
    #    smaller id to that station, and from that station to
    #    station to bigger id
    #
    fareSet = list ( Fare.objects.filter ( Destination_Station = source_station ) )
    fareSet.extend ( list ( Fare.objects.filter ( Source_Station = source_station ) ) )

    #
    # as mentioned above, for fare from bigger station id to smaller
    # one, the source and destination station of the query has to be
    # reversed.
    #
    if ( dest_station.Station_ID > source_station.Station_ID ) :
        fareSet = Fare.objects.filter ( Source_Station = source_station , Destination_Station = dest_station )
    else :
        fareSet = Fare.objects.filter ( Source_Station = dest_station , Destination_Station = source_station )

    return ( fareSet[ 0 ] )

#
#    filter station facilities by preference
#    Input : dictionary of station facilities
#            list of perference category
#            list of perference facilities
#    return : filtered dictionary of station facilities
#
def perf_station_facilities ( facilities , pref_category , pref_facility ) :

    barrcat = BarrCat.objects.all ( )
    pref_facilities = {}

    #
    #    convert the category to category id
    #
    for category in facilities :
        category_set = barrcat.filter ( Category_En = category )
        category_id = category_set[ 0 ].Category_Id
        if ( category_id in pref_category ) :
            is_pref_category = True
        else :
            is_pref_category = False
        for item in facilities [ category ] :
            if is_pref_category :
                is_pref_facility = True
            else :
                #
                #    convert the facility to item_code
                #
                facility_set = barrcat.filter ( Facility_En = item [ "Facility_En" ] )
                facility_item_code = facility_set[ 0 ].Item_Code
                if ( facility_item_code in pref_facility ) :
                    is_pref_facility = True
                else :
                    is_pref_facility = False
            if is_pref_facility :
                facilities_by_cat = pref_facilities.get ( category , [] )
                facilities_by_cat.append ( {
                    "Facility_En" : item [ "Facility_En" ] ,
                    "Adjacent_To" : item [ "Adjacent_To" ] ,
                    } )
                pref_facilities [ category ] = facilities_by_cat

    return ( pref_facilities )

#
#    Register User to system
#    Input : The Post Request from register form
#    Return : True if success,
#             False if username already exists / register failed
#
def registering_user ( request ) :

    username = request.POST.get ( "username" , "" ).strip ( ) # default value = ""
    password = request.POST.get ( "password" , "" ).strip ( )

    if ( username.lower == "guest" ) :
        # Display an information message for invalid username
        messages.info(request, "Invalid username!")
        return ( False )

    # Check if a user with the provided username already exists
    user = User.objects.filter( username = username )

    if user.exists():
        # Display an information message if the username is taken
        messages.info(request, "Username already taken!")
        return ( False )

    # Create a new User object with the provided information
    user = User.objects.create_user ( username = username )
        
    # Set the user's password and save the user object
    user.set_password( password )
    user.save( )
        
    # Display an information message indicating successful account creation
    messages.info(request, "Account created Successfully!")

    return ( True )

#
#    Log User onto the system
#    Input : The Post Request from logon form
#    Return : True if success,
#             False if logon failed
#
def logging_on_user ( request ) :

    username = request.POST.get ( "username" , "" ).strip ( ) # default value = ""
    password = request.POST.get ( "password" , "" ).strip ( )

    # Check if a user with the provided username exists
    if not User.objects.filter(username=username).exists():
        # Display an error message if the username does not exist
        messages.error( request, "Invalid Username" )
        return ( False )
        
    user = authenticate ( username = username , password = password )
        
    if user is None:
        # Display an error message if authentication fails (invalid password)
        messages.error ( request , "Invalid Password" )
        return ( False )
    else:
        login ( request , user )
        return ( True )

#
#    Show the Homepage
#
def showing_homepage ( request ) :

    username = userORguest ( request )
    stations = Station.objects.all ( )

    user = request.user
    userPref = getUserPref ( request )

    context = {
        "username"     : username ,
        "station_list" : stations ,
        "userPref"     : userPref ,
    }
    return ( context )

#
#    Show the fare for selected station
#    Return context for showing fare page
#        False if station not selected or
#        departing and destination station is the same
#
def showing_fare ( request ) :

    username = userORguest ( request )
    userPref = getUserPref ( request )
    source_pref_facilities = {}
    dest_pref_facilities   = {}

    if request.method == "POST" :
        source_station_id = request.POST.get ( "Departing From" , "" )
        dest_station_id = request.POST.get ( "Going To" , "" )

        source_station = Station.objects.get ( Station_ID = source_station_id )
        dest_station = Station.objects.get ( Station_ID = dest_station_id )

        if ( ( dest_station_id == "" ) or ( source_station_id ) == "" ) :
            messages.error( request, "Please select departing and destination stations" )
            return ( False )

        if ( source_station_id == dest_station_id ) :
            messages.error( request, "Departing and destination stations cannot be the same" )
            return ( False )

        fare = getFare ( source_station , dest_station )

        #
        #    get facilities of stations if logged on
        #
        if ( username != "Guest" ) :
            source_station_facilities = station_facilities ( source_station_id )
            dest_station_facilities = station_facilities ( dest_station_id )
            source_pref_facilities = perf_station_facilities ( source_station_facilities , userPref [ "Category" ] , userPref [ "Facility" ] )
            dest_pref_facilities   = perf_station_facilities ( dest_station_facilities   , userPref [ "Category" ] , userPref [ "Facility" ] )

        context = {
            "username" : username ,
            "source_station" : source_station ,
            "dest_station" : dest_station ,
            "card_adult" : fare.Octopus_Card_Adult ,
            "card_student" : fare.Octopus_Card_Student ,
            "card_60" : fare.Octopus_Card_60 ,
            "single_ticket" : fare.Single_Ticket ,
            "card_children" : fare.Octopus_Card_Children ,
            "card_elderly" : fare.Octopus_Card_Elderly ,
            "card_disabled" : fare.Octopus_Card_Disabled ,
            "single_children" : fare.Single_Ticket_Children ,
            "single_elderly" : fare.Single_Ticket_Elderly ,
            "source_pref_facilities" : source_pref_facilities ,
            "dest_pref_facilities" : dest_pref_facilities ,
            }
            
        return ( context )

    return ( False )

#
#    Create the context for displaying barrier free facilities
#
def diplay_barrfac ( request , station_id ) :

    username = userORguest ( request )

    station = get_object_or_404( Station , Station_ID = station_id )

    facilities = station_facilities ( station_id )

    context = { "username" : username ,
                "station" : station ,
                "facilities" : facilities }

    return ( context )


