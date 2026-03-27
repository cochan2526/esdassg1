from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import BarrCat , Station , BarrFac , Fare


# Source - https://stackoverflow.com/a/6761908
# Posted by Manny D
# Retrieved 2026-03-27, License - CC BY-SA 3.0

__all__ = [ "registering_user" ,
            "logging_on_user" ,
            "showing_fare" ,
#             "userORguest" ,
            "showing_homepage" ,
            "diplay_barrfac" ,
          ]

#
#    Return "Guest" if username is not exists ( not logged on )
#
def userORguest ( request ) :
    username = request.user.username
    if ( username == "" ) :
        username = "Guest"
    return ( username )

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

    context = {
        "username"     : username ,
        "station_list" : stations ,
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

    if request.method == "POST" :
        source_station_id = request.POST.get ( "Departing From" , "" )
        dest_station_id = request.POST.get ( "Going To" , "" )

        if ( ( dest_station_id == "" ) or ( source_station_id ) == "" ) :
            messages.error( request, "Please select departing and destination stations" )
            return ( False )

        source_station = Station.objects.get ( Station_ID = source_station_id )
        fareSet = list ( Fare.objects.filter ( Destination_Station = source_station ) )
        fareSet.extend ( list ( Fare.objects.filter ( Source_Station = source_station ) ) )
        
        if ( source_station_id == dest_station_id ) :
            messages.error( request, "Departing and destination stations cannot be the same" )
            return ( False )
        else :
            dest_station = Station.objects.get ( Station_ID = dest_station_id )
            if ( dest_station_id > source_station_id ) :
                fareSet = Fare.objects.filter ( Source_Station = source_station , Destination_Station = dest_station )
            else :
                fareSet = Fare.objects.filter ( Source_Station = dest_station , Destination_Station = source_station )

    fare = fareSet [ 0 ]

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
        }

    return ( context )

#
#    Create the context for displaying barrier free facilities
#
def diplay_barrfac ( request , station_id ) :

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

    return ( context )


