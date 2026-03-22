from django.shortcuts import render , redirect

from django.contrib import messages
from django.contrib.auth.models import User

# from .models import StoryEntry

# Create your views here.

#
#    Register User to system
#    Input : The Post Request from register form
#    Return : True if success, False if username already exists
#
def registering_user ( request ) :

    username = request.POST.get ( "username" , "" ).strip ( ) # default value = ""
    password = request.POST.get ( "password" , "" ).strip ( )

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

