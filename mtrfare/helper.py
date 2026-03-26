from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import BarrCat , Station , BarrFac , Fare

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
#    Show the fare for selected station
#
def showing_fare ( request ) :

    if request.method == "POST" :
        source_station_id = request.POST.get ( "Departing From" , "" )
        source_station = Station.objects.get ( Station_ID = source_station_id )
        fare = list ( Fare.objects.filter ( Destination_Station = source_station ) )
        fare.extend ( list ( Fare.objects.filter ( Source_Station = source_station ) ) )
        
        print ( "Source Station :" , source_station )
        print ( "Fare :" , fare )

        dest_station_id = request.POST.get ( "Going To" , "" )
        if ( ( dest_station_id != "" ) and ( source_station_id != dest_station_id ) ) :
            dest_station = Station.objects.get ( Station_ID = dest_station_id )
            if ( dest_station_id > source_station_id ) :
                fare = Fare.objects.filter ( Source_Station = source_station , Destination_Station = dest_station )
            else :
                fare = Fare.objects.filter ( Source_Station = dest_station , Destination_Station = source_station )
            print ( "Dest Station :" , dest_station )
            print ( "Source station number = " , source_station.Station_ID , " Dest Station number = " , dest_station.Station_ID )
            print ( "Fare :" , fare )

